"""
This file helps to test graphql queries and verify that the "big picture" works
"""
import string
import random
import pytest
from graphene.test import Client
from BuyBitcoin.graphene_schema import SCHEMA
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from trading.models import TradingAccount, Trade
from stocks.models import DailyStockQuote, InvestmentBucket, \
    InvestmentBucketDescription, InvestmentStockConfiguration, Stock
from stocks.historical import create_stock
from graphql_relay.node.node import to_global_id


def request_create(request):
    """
    Creates a fully functional environment that we can test on
    """
    post_save.disconnect(receiver=create_stock, sender=Stock)
    stock = Stock(name="Google", ticker="GOOGL")
    stock.save()

    pw2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
    user2 = User.objects.create(username='testuser2', password=pw2)
    account2 = TradingAccount(profile=user2.profile, account_name="testAccount2")
    account2.save()
    trade2 = Trade(quantity=2, account=account2, stock=stock)
    trade2.save()

    pw1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
    request.user = User.objects.create(username='testuser1', password=pw1)
    account1 = TradingAccount(profile=request.user.profile, account_name="testAccount1")
    account1.save()
    trade1 = Trade(quantity=1, account=account1, stock=stock)
    trade1.save()

    bucket = InvestmentBucket(name="i1", public=False, available=100, owner=request.user.profile)
    bucket.save()
    InvestmentBucketDescription(text="Blabla", is_good=True, bucket=bucket).save()
    DailyStockQuote(value=9, date="2017-05-08", stock=stock).save()
    DailyStockQuote(value=10, date="2017-05-10", stock=stock).save()
    InvestmentStockConfiguration(stock=stock, quantity=1, bucket=bucket, start="2017-05-09").save()

    return request


@pytest.mark.django_db(transaction=True)
# pylint: disable=invalid-name
def test_mutation_add_trading_account(rf, snapshot):
    """
    Tests the mutation to add a trading account
    """
    # pylint: enable=invalid-name
    request = rf.post('/graphql')
    pw1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
    request.user = User.objects.create(username='testuser1', password=pw1)
    client = Client(SCHEMA)
    acc_name = "Test 1"
    executed = client.execute("""
        mutation {{
          addTradingAccount(name: "{}") {{
            account {{
              accountName
            }}
          }}
        }}
    """.format(acc_name), context_value=request)
    snapshot.assert_match(executed)
    acc = TradingAccount.objects.get(profile__user__id=request.user.id)
    ex_acc = executed['data']['addTradingAccount']['account']['accountName']
    assert ex_acc == acc.account_name


@pytest.mark.django_db(transaction=True)
# pylint: disable=invalid-name
def test_mutation_add_bucket(rf, snapshot):
    """
    This submits a massive graphql query to verify all fields work
    """
    # pylint: enable=invalid-name
    request = rf.post('/graphql')
    pw1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
    request.user = User.objects.create(username='testuser1', password=pw1)
    client = Client(SCHEMA)
    acc_name = "Test 1"
    investment = 333.33
    executed = client.execute("""
        mutation {{
          addBucket(name: "{}", investment: {}, public: true) {{
            bucket {{
                available
                isOwner
                public
                name
            }}
          }}
        }}
    """.format(acc_name, investment), context_value=request)
    snapshot.assert_match(executed)
    acc = InvestmentBucket.objects.all()[0]
    ex_acc = executed['data']['addBucket']['bucket']['available']
    assert (ex_acc == acc.available) and (investment == ex_acc)


@pytest.mark.django_db(transaction=True)
# pylint: disable=invalid-name
def test_mutation_add_stock_to_bucket(rf, snapshot):
    """
    This submits a massive graphql query to verify all fields work
    """
    # pylint: enable=invalid-name
    request = rf.post('/graphql')
    pw1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
    request.user = User.objects.create(username='testuser1', password=pw1)
    bucket = InvestmentBucket(name="i1", public=False, available=100, owner=request.user.profile)
    bucket.save()
    post_save.disconnect(receiver=create_stock, sender=Stock)
    stock = Stock(name="Google", ticker="GOOGL")
    stock.save()
    DailyStockQuote(value=9, date="2017-05-08", stock=stock).save()
    DailyStockQuote(value=10, date="2017-05-10", stock=stock).save()
    DailyStockQuote(value=9, date="2017-05-09", stock=stock).save()
    client = Client(SCHEMA)
    executed = client.execute(
        """
            mutation {{
              addStockToBucket(stockId: "{}", bucketId: "{}", quantity: {}) {{
                bucket {{
                    available
                    isOwner
                    public
                    name
                    stocks {{
                        edges {{
                            node {{
                                quantity
                                stock {{
                                    ticker
                                }}
                            }}
                        }}
                    }}
                }}
              }}
            }}
        """.format(
            to_global_id("GStock", stock.id),
            to_global_id("GInvestmentBucket", bucket.id), 3.5
        ),
        context_value=request
    )
    snapshot.assert_match(executed)
    assert InvestmentStockConfiguration.objects.count() == 1


@pytest.mark.django_db(transaction=True)
# pylint: disable=invalid-name
def test_mutation_add_attribute_to_investment(rf, snapshot):
    """
    This submits a massive graphql query to verify all fields work
    """
    # pylint: enable=invalid-name
    request = rf.post('/graphql')
    pw1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
    request.user = User.objects.create(username='testuser1', password=pw1)
    bucket = InvestmentBucket(name="i1", public=False, available=100, owner=request.user.profile)
    bucket.save()
    client = Client(SCHEMA)
    executed = client.execute("""
        mutation {{
          addAttributeToBucket(desc: "{}", bucketId: "{}", isGood: true) {{
            bucketAttr {{
                text
                isGood
            }}
          }}
        }}
    """.format("Test Desc", to_global_id("GInvestmentBucket", bucket.id)), context_value=request)
    snapshot.assert_match(executed)
    assert InvestmentBucketDescription.objects.count() == 1


@pytest.mark.django_db(transaction=True)
# pylint: disable=invalid-name
def test_mutation_attribute_permission(rf, snapshot):
    """
    This submits a massive graphql query to verify all fields work
    """
    # pylint: enable=invalid-name
    request = rf.post('/graphql')
    pw2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
    user2 = User.objects.create(username='testuser2', password=pw2)
    pw1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
    request.user = User.objects.create(username='testuser1', password=pw1)
    bucket = InvestmentBucket(name="i1", public=False, available=100, owner=user2.profile)
    bucket.save()
    attr = InvestmentBucketDescription(text="desc1", bucket=bucket, is_good=True)
    attr.save()
    client = Client(SCHEMA)
    executed = client.execute("""
        mutation {{
          addAttributeToBucket(desc: "{}", bucketId: "{}", isGood: true) {{
            bucketAttr {{
                isGood
            }}
          }}
        }}
    """.format("Test Desc", to_global_id("GInvestmentBucket", bucket.id)), context_value=request)
    snapshot.assert_match(executed)
    executed = client.execute(
        """
            mutation {{
              editAttribute(desc: "{}", idValue: "{}") {{
                bucketAttr {{
                    isGood
                }}
              }}
            }}
        """.format(
            "Test Desc",
            to_global_id("GInvestmentBucketDescription", attr.id)
        ),
        context_value=request
    )
    snapshot.assert_match(executed)
    executed = client.execute("""
        mutation {{
          deleteAttribute(idValue: "{}") {{
            isOk
          }}
        }}
    """.format(to_global_id("GInvestmentBucketDescription", attr.id)), context_value=request)
    snapshot.assert_match(executed)
    executed = client.execute(
        """
            mutation {{
              addStockToBucket(stockId: "{}", bucketId: "{}", quantity: {}) {{
                bucket {{
                  id
                }}
              }}
            }}
        """.format(
            to_global_id("GStock", 1),
            to_global_id("GInvestmentBucket", bucket.id), 3.5
        ),
        context_value=request
    )
    snapshot.assert_match(executed)
    assert InvestmentBucketDescription.objects.count() == 1


@pytest.mark.django_db(transaction=True)
# pylint: disable=invalid-name
def test_mutation_edit_attribute(rf, snapshot):
    """
    This submits a massive graphql query to verify all fields work
    """
    # pylint: enable=invalid-name
    request = rf.post('/graphql')
    pw1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
    request.user = User.objects.create(username='testuser1', password=pw1)
    bucket = InvestmentBucket(name="i1", public=False, available=100, owner=request.user.profile)
    bucket.save()
    attr = InvestmentBucketDescription(text="Blabla", is_good=True, bucket=bucket)
    attr.save()
    client = Client(SCHEMA)
    executed = client.execute(
        """
            mutation {{
              editAttribute(desc: "{}", idValue: "{}") {{
                bucketAttr {{
                    text
                    isGood
                }}
              }}
            }}
        """.format(
            "Test Desc",
            to_global_id("GInvestmentBucketDescription", attr.id)
        ),
        context_value=request
    )
    snapshot.assert_match(executed)


@pytest.mark.django_db(transaction=True)
# pylint: disable=invalid-name
def test_mutation_delete_attribute(rf, snapshot):
    """
    This submits a massive graphql query to verify all fields work
    """
    # pylint: enable=invalid-name
    request = rf.post('/graphql')
    pw1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
    request.user = User.objects.create(username='testuser1', password=pw1)
    bucket = InvestmentBucket(name="i1", public=False, available=100, owner=request.user.profile)
    bucket.save()
    attr = InvestmentBucketDescription(text="Blabla", is_good=True, bucket=bucket)
    attr.save()
    client = Client(SCHEMA)
    executed = client.execute("""
        mutation {{
          deleteAttribute(idValue: "{}") {{
            isOk
          }}
        }}
    """.format(to_global_id("GInvestmentBucketDescription", attr.id)), context_value=request)
    snapshot.assert_match(executed)
    assert InvestmentBucketDescription.objects.all().count() == 0


@pytest.mark.django_db(transaction=True)
# pylint: disable=invalid-name
def test_mutation_edit_configuration(rf, snapshot):
    """
    This submits a massive graphql query to verify all fields work
    """
    # pylint: enable=invalid-name
    request = rf.post('/graphql')
    pw1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
    request.user = User.objects.create(username='testuser1', password=pw1)
    bucket = InvestmentBucket(name="i1", public=False, available=100, owner=request.user.profile)
    bucket.save()
    post_save.disconnect(receiver=create_stock, sender=Stock)
    stock = Stock(name="Google", ticker="GOOGL")
    stock.save()
    DailyStockQuote(value=9, date="2017-05-08", stock=stock).save()
    DailyStockQuote(value=10, date="2017-05-10", stock=stock).save()
    InvestmentStockConfiguration(stock=stock, quantity=1, bucket=bucket, start="2017-05-09").save()
    client = Client(SCHEMA)
    executed = client.execute(
        """
            mutation {{
              editConfiguration(idValue: "{}", config: [
                {{idValue: "{}", quantity: {}}}
              ]) {{
                bucket {{
                    name
                    available
                }}
              }}
            }}
        """.format(
            to_global_id("GInvestmentBucket", bucket.id),
            to_global_id("GStock", stock.id),
            2
        ),
        context_value=request
    )
    snapshot.assert_match(executed)
    assert InvestmentStockConfiguration.objects.all().count() == 2


@pytest.mark.django_db(transaction=True)
# pylint: disable=invalid-name
def test_big_gql(rf, snapshot):
    """
    This submits a massive graphql query to verify all fields work
    """
    # pylint: enable=invalid-name
    request = request_create(rf.post('/graphql'))
    client = Client(SCHEMA)
    executed = client.execute("""
{
  viewer {
    id
    username
    profile {
      investSuggestions {
        edges {
          node {
            id
            name
            public
            available
            isOwner
            description {
              edges {
                node {
                  id
                  text
                  isGood
                }
              }
            }
            stocks {
              edges {
                node {
                  id
                  quantity
                  stock {
                    name
                    latestQuote {
                      value
                    }
                  }
                  start
                  end
                }
              }
            }
          }
        }
      }
      stockFind(text: "GO") {
        id
        quoteInRange(start: "2017-05-07", end: "2017-05-11") {
          value
          date
        }
      }
      tradingAccounts {
        edges {
          node {
            accountName
            trades {
              edges {
                node {
                  quantity
                  stock {
                    ticker
                    name
                    trades {
                      edges {
                        node {
                          account {
                            accountName
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
    """, context_value=request)
    snapshot.assert_match(executed)

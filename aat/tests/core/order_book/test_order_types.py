from datetime import datetime
from aat.config import Side, DataType, OrderType
from aat.core import Instrument, OrderBook, Order
from .helpers import _seed


_INSTRUMENT = Instrument('TE.ST')


class TestMarketOrder:
    def test_order_book_market_order(self):
        ob = OrderBook(_INSTRUMENT)

        _seed(ob, _INSTRUMENT)

        assert ob.topOfBook()['bid'] == (5.0, 1.0)
        assert ob.topOfBook()['ask'] == (5.5, 1.0)

        data = Order(id=1,
                     timestamp=datetime.now().timestamp(),
                     volume=100.0,
                     price=0.0,
                     side=Side.SELL,
                     type=DataType.ORDER,
                     order_type=OrderType.MARKET,
                     instrument=_INSTRUMENT,
                     exchange='')
        ob.add(data)

        print(ob)
        print(ob.topOfBook())
        assert ob.topOfBook() == {'bid': (0, 0), 'ask': (5.5, 1.0)}
        print(ob.levels(3))
        assert ob.levels(3) == {'bid': [(0, 0)], 'ask': [(5.5, 1.0), (5.5, 1.0), (6.0, 1.0), (6.5, 1.0)]}


class TestStopLoss:
    def test_stop_limit(self):
        ob = OrderBook(_INSTRUMENT)

        _seed(ob, _INSTRUMENT)

        assert ob.topOfBook()['bid'] == (5.0, 1.0)
        assert ob.topOfBook()['ask'] == (5.5, 1.0)

        print(ob)
        assert ob.topOfBook() == {"bid": (5.0, 1.0), 'ask': (5.5, 1.0)}

        data = Order(id=1,
                     timestamp=datetime.now().timestamp(),
                     volume=0.0,
                     price=5.0,
                     side=Side.SELL,
                     type=DataType.ORDER,
                     order_type=OrderType.STOP_MARKET,
                     stop_target=Order(
                         id=1,
                         timestamp=datetime.now().timestamp(),
                         volume=1.0,
                         price=4.0,
                         side=Side.SELL,
                         type=DataType.ORDER,
                         order_type=OrderType.MARKET,
                         instrument=_INSTRUMENT,
                         exchange=''
                     ),
                     instrument=_INSTRUMENT,
                     exchange='')
        print(ob)
        ob.add(data)

        data = Order(id=1,
                     timestamp=datetime.now().timestamp(),
                     volume=0.0,
                     price=5.0,
                     side=Side.SELL,
                     type=DataType.ORDER,
                     order_type=OrderType.STOP_LIMIT,
                     stop_target=Order(
                         id=1,
                         timestamp=datetime.now().timestamp(),
                         volume=0.5,
                         price=5.0,
                         side=Side.SELL,
                         type=DataType.ORDER,
                         instrument=_INSTRUMENT,
                         exchange=''
                     ),
                     instrument=_INSTRUMENT,
                     exchange='')
        print(ob)
        ob.add(data)

        print(ob.topOfBook())
        assert ob.topOfBook() == {"bid": (5.0, 1.0), "ask": (5.5, 1.0)}

        data = Order(id=1,
                     timestamp=datetime.now().timestamp(),
                     volume=0.5,
                     price=5.0,
                     side=Side.SELL,
                     type=DataType.ORDER,
                     order_type=OrderType.LIMIT,
                     instrument=_INSTRUMENT,
                     exchange='')
        print(ob)
        ob.add(data)

        print(ob.topOfBook())
        assert ob.topOfBook() == {"bid": (4.5, 0.5), "ask": (5.0, 0.5)}

    def test_stop_market(self):
        ob = OrderBook(_INSTRUMENT)

        _seed(ob, _INSTRUMENT)

        assert ob.topOfBook()['bid'] == (5.0, 1.0)
        assert ob.topOfBook()['ask'] == (5.5, 1.0)

        print(ob)
        assert ob.topOfBook() == {"bid": (5.0, 1.0), 'ask': (5.5, 1.0)}

        data = Order(id=1,
                     timestamp=datetime.now().timestamp(),
                     volume=0.0,
                     price=5.0,
                     side=Side.SELL,
                     type=DataType.ORDER,
                     order_type=OrderType.STOP_LIMIT,
                     stop_target=Order(
                         id=1,
                         timestamp=datetime.now().timestamp(),
                         volume=0.5,
                         price=4.5,
                         side=Side.SELL,
                         type=DataType.ORDER,
                         instrument=_INSTRUMENT,
                         exchange=''
                     ),
                     instrument=_INSTRUMENT,
                     exchange='')
        print(ob)
        ob.add(data)

        print(ob.topOfBook())
        assert ob.topOfBook() == {"bid": (5.0, 1.0), "ask": (5.5, 1.0)}

        data = Order(id=1,
                     timestamp=datetime.now().timestamp(),
                     volume=0.5,
                     price=5.0,
                     side=Side.SELL,
                     type=DataType.ORDER,
                     order_type=OrderType.LIMIT,
                     instrument=_INSTRUMENT,
                     exchange='')
        print(ob)
        ob.add(data)

        print(ob.topOfBook())
        assert ob.topOfBook() == {"bid": (4.5, 1.0), "ask": (5.5, 1.0)}
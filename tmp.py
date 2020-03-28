from datetime import datetime
from aat.config import Side, DataType
from aat.core import Instrument, OrderBook, Order
from aat.core.order_book import _insort, _PriceLevel

_INSTRUMENT = Instrument('TE.ST')        


ob = OrderBook(_INSTRUMENT)

x = .5
while x < 10.0:
    side = Side.BUY if x <= 5 else Side.SELL
    ob.add(Order(id=1,
                timestamp=datetime.now().timestamp(),
                volume=1.0,
                price=x,
                side=side,
                type=DataType.ORDER,
                instrument=_INSTRUMENT,
                exchange=''))
    x += .5

assert ob.topOfBook()['bid'] == (5.0, 1.0)
assert ob.topOfBook()['ask'] == (5.5, 1.0)

data = Order(id=1,
            timestamp=datetime.now().timestamp(),
            volume=100.0,
            price=0.0,
            side=Side.SELL,
            type=DataType.ORDER,
            instrument=_INSTRUMENT,
            exchange='')
ob.add(data)

print(ob)
assert ob.topOfBook() == {"bid": (0.0, 0.0), "ask": (4.5, 3.0)}
print(ob.levels(3))
assert ob.levels(3) == {'bid': [], 'ask': [(4.5, 3.0), (4.5, 3.0), (5.5, 1.0), (6.0, 1.0)]}
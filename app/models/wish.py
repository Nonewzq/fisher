from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, desc
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func

from app.models.base import Base, db
from app.models.gift import Gift
from app.spider.yushu_book import YuShuBook


class Wish(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    @classmethod
    def get_my_wish(cls, uid):
        wish = Wish.query.filter_by(uid=uid,
                                    launched=False
                                    ).order_by(desc(Wish.create_time)).all()
        return wish

    @classmethod
    def get_gift_count(cls, isbn_list):
        gift_list = db.session.query(func.count(Gift.isbn), Gift.isbn).filter(
            Gift.launched == False,
            Gift.isbn.in_(isbn_list),
            Gift.status == 1).group_by(Gift.isbn).all()
        gift_count = [{'count': w[0], 'isbn': w[1]}for w in gift_list]
        return gift_count

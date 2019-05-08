from app.view_models.book import BookViewModel


class MyWishes:
    def __init__(self, my_wishes, my_gift_count):
        self.wishes = []
        self.my_wishes = my_wishes
        self.my_gift_count = my_gift_count
        self.wishes = self.__parse()

    def __parse(self):
        temp_wishes = []
        for gift in self.my_wishes:
            my_gift = self.__matching(gift)
            temp_wishes.append(my_gift)
        return temp_wishes

    def __matching(self, gift):
        count = 0
        for gift_count in self.my_gift_count:
            if gift_count['isbn'] == gift.isbn:
                count = gift_count['count']
        r = {
            'wishes_count': count,
            'book': BookViewModel(gift.book),
            'id': gift.id
        }
        return r


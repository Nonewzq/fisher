from app.view_models.book import BookViewModel


class MyGifts:
    def __init__(self, gifts_of_mine, wish_count_list ):
        self.gifts = []
        self.gifts_of_mine = gifts_of_mine
        self.wish_count_list = wish_count_list
        self.gifts = self.__parse()

    def __parse(self):
        temp_gift = []
        for gift in self.gifts_of_mine:
            my_gift = self.__matching(gift)
            temp_gift.append(my_gift)
        return temp_gift

    def __matching(self, gift):
        count = 0
        for wish_count in self.wish_count_list:
            if gift.isbn == wish_count['isbn']:
                count = wish_count['count']
        r = {'wishes_count': count,
             'book': BookViewModel(gift.book),
             'id': gift.id}
        return r


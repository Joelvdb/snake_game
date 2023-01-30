from typing import List, Any, Tuple


class Link:
    """
    represents the object that the snake is made of
    """

    def __init__(self, location: Tuple) -> None:
        """
        :param color: color of link
        :param location: location of link
        """
        self.location = location


class Snake:
    """
    the snake in Snake game, build as a list of Links
    """

    def __init__(self, location: List[Tuple], length=3, color="black") -> None:
        """
        :param location: a list of tuples contains the location of every link that the snake is made of
        :param length: the length of the snake - number of links that it is made of
        :param color: color of the snake
        """
        self.location = location
        self.length = length
        self.color = color
        self.ate_apple = False
        self.direction = "Up"
        self.links = []
        for i in range(length):
            link_location = (location[0], location[1] - i)
            link = Link(link_location)
            self.links.append(link)

    def get_head_location(self):
        # returns the location of the first link in the snakes links list
        return self.location[0]

    def change_ate_apple(self, bool: bool):
        # changes th boolean expression that indicates if the snake ate an apple or not, if it should grow or not
        self.ate_apple = bool

    def check_collide(self):
        """
        :return: True if the snake collide into itself, False otherwise
        """
        for i in range(len(self.links) - 1):
            if self.links[i].location in self._get_links_coordinates(self.links[i + 1:]):
                return True
        return False

    def cut_head(self):
        self.links.remove(self.links[0])


    def get_coordinates(self):
        """
        :return: the coordinates of all links in snake
        """
        coor_list = self._get_links_coordinates(self.links)
        return coor_list

    def _get_links_coordinates(self, links: List):
        """
        :param links: list pf links
        :return:list of coordinates of the links
        """
        coor_list = []
        for link in links:
            coor_list.append(link.location)
        return coor_list

    def move_snake(self, move_direction: str, ate_apple=False) -> None:
        """
        :param direction: the direction the snake should move
        changes snake coordinates according to the move
        if ate_apple is True it doesnt remove the snakes last link after a move
        """
        new_link_location = []
        cur_row = self.location[1]
        cur_col = self.location[0]
        if not move_direction:
            move_direction = self.direction

        not_legal_moves = [["Down", "Up"], ["Right", "Left"]]
        for moves in not_legal_moves:
            if self.direction in moves and move_direction in moves:
                move_direction = self.direction

        if move_direction == "Up":
            new_link_location = (cur_col, cur_row + 1)
        if move_direction == "Down":
            new_link_location = (cur_col, cur_row - 1)
        if move_direction == "Right":
            new_link_location = (cur_col + 1, cur_row)
        if move_direction == "Left":
            new_link_location = (cur_col - 1, cur_row)

        if 0 <= new_link_location[0] < 40 and 0 <= new_link_location[1] < 30 :
            self.location = new_link_location
            self.direction = move_direction
            new_link = Link(new_link_location)
            self.links.insert(0, new_link)
            if not self.ate_apple:
                self.links.remove(self.links[len(self.links) - 1])
            return True
        else:
            self.links.remove(self.links[len(self.links) - 1])
            return False

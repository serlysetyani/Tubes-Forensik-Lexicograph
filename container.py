class container(object):
    def __init__(self) -> None:
        self.container_list = []
        return

    def length(self):
        return len(self.container_list)

    def add_block(self, data):
        self.container_list.append(data)
        return

    def sort_feature(self):
        self.container_list = sorted(
            self.container_list, key=lambda x: (x[1], x[2]))
        return

    def print_all(self):
        for i in range(0, self.length()):
            print(self.container_list[i])
        return

    def print_container(self, iter):
        print(f"Elemen ke-{self.length()}")
        if iter < self.length():
            for i in range(0, iter):
                print(self.container_list[i])
        else:
            self.print_all()
        return

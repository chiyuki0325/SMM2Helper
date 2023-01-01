from SMM2 import encryption
from SMM2 import course

def main():
        import sys

        filename = sys.argv[1]
        data = open(filename, "rb").read()

        SMM2Course = encryption.Course(data)
        SMM2Course.decrypt()
        SMM2Course = course.Course(SMM2Course.data)

        print(SMM2Course.HEADER.GAME_STYLE)
        print(SMM2Course.HEADER.SAVE_DATE, SMM2Course.HEADER.SAVE_TIME)
        print(SMM2Course.HEADER.NAME)
        print(SMM2Course.HEADER.DESCRIPTION)
        print(SMM2Course.HEADER.TIME_LIMIT)

        for Actor in SMM2Course.OVERWORLD.ACTORS:
                print(Actor.POSITION)
                print(Actor.SIZE)
                print(Actor.FLAGS)
                print(Actor.EXTENDED_DATA)
                print(Actor.TYPES)
                print(Actor.LINK_ID)
                print(Actor.OTOASOBI_ID)

        for Actor in SMM2Course.SUBWORLD.ACTORS:
                print(Actor.POSITION)
                print(Actor.SIZE)
                print(Actor.FLAGS)
                print(Actor.EXTENDED_DATA)
                print(Actor.TYPES)
                print(Actor.LINK_ID)
                print(Actor.OTOASOBI_ID)

if __name__ == "__main__":
        main()

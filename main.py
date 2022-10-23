# from game import charactor
import manage, sys

# 서버 열기 python manage.py runserver
if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.argv.append('runserver')
    manage.main()


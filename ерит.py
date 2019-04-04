# apteka поиск ближайшей
from mygeocoder import *
from mymapapi import *
import sys


def main():
    # not todo but:
    to_find = ' '.join(sys.argv[1:])
    # ^v^
    if to_find:
        ll, spn = get_spn(to_find)
        the_coolest_one = '{}&spn={}'.format(ll, spn)
        
        chemists = corporation_finder(ll, spn, 'аптека')
        
        c = get_coordinates(chemists)
        the_garden = 'pt={},{},pmrdl1'.format(c[0], c[1])
        show_map(the_coolest_one, 'sat', the_garden)
    

if __name__ == '__main__':
    main()
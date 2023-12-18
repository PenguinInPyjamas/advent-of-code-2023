import argparse
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])


def read_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path")
    args = parser.parse_args()
    galaxy_locations = parse_star_image("".join(open(args.input_file_path)))
    return galaxy_locations


def parse_star_image(star_image):
    galaxy_locations = set()
    for y, star_image_row in enumerate(star_image.split("\n")):
        for x, char in enumerate(star_image_row):
            if char == "#":
                galaxy_locations.add(Point(x, y))
    return galaxy_locations


def main():
    galaxy_locations = read_input()
    expanded_image = expand_galaxies(galaxy_locations)
    print(f"Part 1: {int(sum(abs(a.x - b.x) + abs(a.y - b.y) for a in expanded_image for b in expanded_image) / 2)}")
    more_expanded_image = expand_galaxies(galaxy_locations, 1000000)
    print(f"Part 2: {int(sum(abs(a.x - b.x) + abs(a.y - b.y) for a in more_expanded_image for b in more_expanded_image) / 2)}")


def expand_galaxies(original_galaxy_locations, expansion_factor=2):
    expanded_rows = set()
    expanded_columns = set()

    for x in range(max(p.x for p in original_galaxy_locations) + 1):
        if not any(p.x == x for p in original_galaxy_locations):
            expanded_rows.add(x)

    for y in range(max(p.y for p in original_galaxy_locations) + 1):
        if not any(p.y == y for p in original_galaxy_locations):
            expanded_columns.add(y)

    return {Point(p.x + sum(expansion_factor - 1 if x in expanded_rows else 0 for x in range(p.x)),
                  p.y + sum(expansion_factor - 1 if y in expanded_columns else 0 for y in range(p.y)))
            for p in original_galaxy_locations}


if __name__ == "__main__":
    main()

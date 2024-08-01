import numpy as np
from scipy.spatial.distance import cdist
from PIL import Image
import sys

input_image = sys.argv[1]
output_image = sys.argv[2]
divisor = int(sys.argv[3])

i = Image.open(input_image)
ii = np.array(i)
iii = np.where(ii==1)
iiii = np.column_stack(list(reversed(iii)))
iiiii = iiii[np.random.choice(iiii.shape[0],iiii.shape[0]//divisor,replace=False),:]

the_first = iiiii[0]
first_mask  = np.ones(iiiii.shape[0], dtype=bool)
first_mask[[0]] = False
the_rest = iiiii[first_mask]
collection = np.array([the_first])

for x in range(iiiii.shape[0]-1):
    all_distances = cdist(the_rest, [the_first])
    next_distance = np.min(all_distances)
    distance_match = np.where(all_distances == next_distance)[0][0]
    found_next = the_rest[distance_match]
    collection = np.concatenate([collection,np.array([found_next])])
    next_mask  = np.ones(the_rest.shape[0], dtype=bool)
    next_mask[[distance_match]] = False
    next_rest  = the_rest[next_mask]
    next_first = found_next
    the_first = found_next
    the_rest  = next_rest

svg_template = '<svg width="{}" height="{}" xmlns="http://www.w3.org/2000/svg">{}</svg>'
path_template = '<path d="{}" fill="none" stroke="black" />"'
move_template = 'M {} {} '
line_template = 'L {} {} '

path_string = move_template.format(*collection[0])
for x in collection[1:]:
    path_string += line_template.format(*x)

final_svg = svg_template.format(
        i.width,
        i.height,
        path_template.format(path_string)
        )

with open(output_image,'w') as f:
    f.write(final_svg)


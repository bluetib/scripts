#!/usr/bin/env python
# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt
from matplotlib.mlab import csv2rec
from matplotlib.cbook import get_sample_data
import json
import functions as func
import sys,os
from pylab import *

#mpl.rcParams['font.sans-serif'] = ['simhei']
myfont = matplotlib.font_manager.FontProperties(fname='/root/simhei.ttf')
mpl.rcParams['axes.unicode_minus'] = False

# fname = get_sample_data('percent_bachelors_degrees_women_usa.csv')
# gender_degree_data = csv2rec(fname)

aa = json.loads(open("/tmp/f_p.txt").read())

# These are the colors that will be used in the plot
color_sequence = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
                  '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
                  '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
                  '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5']

# You typically want your plot to be ~1.33x wider than tall. This plot
# is a rare exception because of the number of lines being plotted on it.
# Common sizes: (10, 7.5) and (12, 9)
fig, ax = plt.subplots(1, 1, figsize=(12, 14))

# Remove the plot frame lines. They are unnecessary here.
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

# Ensure that the axis ticks only show up on the bottom and left of the plot.
# Ticks on the right and top of the plot are generally unnecessary.
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()

# Limit the range of the plot to only where the data is.
# Avoid unnecessary whitespace.
# plt.xlim(1968.5, 2011.1)
# plt.ylim(-0.25, 90)
plt.xlim(0, 25)
plt.ylim(1000, 50000)

# Make sure your axis ticks are large enough to be easily read.
# You don't want your viewers squinting to read your plot.
plt.xticks(range(0, 24, 1), fontsize=14)
# plt.yticks(range(0, 91, 10), ['{0}%'.format(x)
#                               for x in range(0, 91, 10)], fontsize=14)
plt.yticks(range(1000, 50000, 1500), fontsize=14)
# Provide tick lines across the plot to help your viewers trace along
# the axis ticks. Make sure that the lines are light and small so they
# don't obscure the primary data lines.
for y in range(1000, 50000, 1500):
    plt.plot(range(0, 24, 1), [y] * len(range(0, 24, 1)), '--',
             lw=0.5, color='black', alpha=0.3)

# Remove the tick marks; they are unnecessary with the tick lines we just
# plotted.
plt.tick_params(axis='both', which='both', bottom='off', top='off',
                labelbottom='on', left='off', right='off', labelleft='on')

# Now that the plot is prepared, it's time to actually plot the data!
# Note that I plotted the majors in order of the highest % in the final year.
majors = ['Health Professions', 'Public Administration', 'Education',
          'Psychology', 'Foreign Languages', 'English',
          'Communications\nand Journalism', 'Art and Performance', 'Biology',
          'Agriculture', 'Social Sciences and History', 'Business',
          'Math and Statistics', 'Architecture', 'Physical Sciences',
          'Computer Science', 'Engineering']

cities = ["北京","上海","广州","深圳","昆明","杭州","苏州","厦门","南京","西安","珠海","惠州","长沙","武汉","三亚"]

majors = []
for ti in cities:
    majors.append("%s_二手房" % ti)
    majors.append("%s_新房" % ti)

y_offsets = {'Foreign Languages': 0.5, 'English': -0.5,
             'Communications\nand Journalism': 0.75,
             'Art and Performance': -0.25, 'Agriculture': 1.25,
             'Social Sciences and History': 0.25, 'Business': -0.75,
             'Math and Statistics': 0.75, 'Architecture': -0.75,
             'Computer Science': 0.75, 'Engineering': -0.25}

y_offsets = {u'北京_新房': 500, u"上海_二手房":-500, u"杭州_二手房":-100,u"广州_二手房":500,u"苏州_二手房":100,u"南京_二手房":-770,u"珠海_新房":-300,u"珠海_二手房":-800,u"昆明_二手房":400,u"昆明_新房":350,u"惠州_新房":-10,u"西安_二手房":-1200,u"西安_新房":-1100,u"惠州_二手房":-1700,u"苏州_新房":-1200,u"南京_二手房":-800,u"长沙_二手房":50,"长沙_新房":10}

print len(y_offsets)
print len(majors)
print len(cities)
print len(color_sequence)

#sys.exit()

#func.a_list_of_date(func.get_this)
cc = func.get_this_month_first_day_to_last()[0].strftime("%Y-%m")
bb = func.a_list_of_date(cc,24)
bb.reverse()

for rank, column in enumerate(aa.keys()):
    # Plot each line separately with its own color.
#     column_rec_name = column.replace('\n', '_').replace(' ', '_').lower()

    line = plt.plot([ft for ft in range(24)],
                    aa[column]['new'],
                    lw=2.5,
                    color=color_sequence[rank])

    # Add a text label to the right end of every line. Most of the code below
    # is adding specific offsets y position because some labels overlapped.
    y_pos = int(aa[column]['new'][-1])

    if u"%s_新房" % column in y_offsets:
          y_pos += y_offsets[u"%s_新房" % column]

    # Again, make sure that all labels are large enough to be easily read
    # by the viewer.
    plt.text(24, y_pos, "%s_%s" % (column,u"新房"), fontsize=9, color=color_sequence[rank],fontproperties=myfont)
    # Plot each line separately with its own color.
#     column_rec_name = column.replace('\n', '_').replace(' ', '_').lower()

    line = plt.plot([ft for ft in range(24)],
                    aa[column]['second'],
                    lw=2.5,
                    color=color_sequence[-(rank+1)])

    # Add a text label to the right end of every line. Most of the code below
    # is adding specific offsets y position because some labels overlapped.
    y_pos = int(aa[column]['second'][-1])

    if u"%s_二手房" % column in y_offsets:
          y_pos += y_offsets[u"%s_二手房" % column]

    # Again, make sure that all labels are large enough to be easily read
    # by the viewer.
    plt.text(24, y_pos, "%s_%s" % (column,u"二手房"), fontsize=9, color=color_sequence[-(rank+1)],fontproperties=myfont)

# Make the title big enough so it spans the entire plot, but don't make it
# so big that it requires two lines to show.

# Note that if the title is descriptive enough, it is unnecessary to include
# axis labels; they are self-evident, in this plot's case.
plt.title(u'房价', fontsize=18, ha='center',fontproperties=myfont)

# Finally, save the figure as a PNG.
# You can also save it as a PDF, JPEG, etc.
# Just change the file extension in this call.
plt.savefig('f_p.png', bbox_inches='tight')


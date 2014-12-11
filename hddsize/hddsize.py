from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManager
from django.template import loader, Context
from django.db.models import Count
from server.models import *
from django.shortcuts import get_object_or_404
import server.utils as utils

class HDDSize(IPlugin):
    def show_widget(self, page, machines=None, theid=None):

        if page == 'front':
            t = loader.get_template('thomasbergmann/hddsize/templates/front.html')
	    if not machines:
                machines = Machine.objects.all()
        if page == 'bu_dashboard':
            t = loader.get_template('thomasbergmann/hddsize/templates/id.html')
	    if not machines:
                machines = utils.getBUmachines(theid)
        if page == 'group_dashboard':
            t = loader.get_template('thomasbergmann/hddsize/templates/id.html')
	    if not machines:
                machine_group = get_object_or_404(MachineGroup, pk=theid)
                machines = Machine.objects.filter(machine_group=machine_group)

	if machines:
            hddsize_128 = machines.filter(hd_total__lte=117649480).count()
            hddsize_256 = machines.filter(hd_total__range=["117649481", "244277768"]).count()
            hddsize_512 = machines.filter(hd_total__range=["244277769", "975922975"]).count()
	    hddsize_1024 = machines.filter(hd_total__gte=975922976).count()
        else:
            hddsize_128 = 0
            hddsize_256 = 0
            hddsize_512 = 0
	    hddsize_1024 = 0

	c = Context({
            'title': 'Disk Size',
            '128_label': '128GB',
            '128_count': hddsize_128,
	    '256_label': '256GB',
            '256_count': hddsize_256,
	    '512_label': '512GB',
            '512_count': hddsize_512,
	    '1024_label': '1024GB +',
            '1024_count': hddsize_1024,
            'plugin': 'HDDSize',
	    'page': page,
            'theid': theid
        })
        return t.render(c), 4 

    def filter_machines(self, machines, data):
	if data == '128':
            machines = machines.filter(hd_total__lt=117649480)
            title = 'Machines with 128GB Harddisk'

        elif data == '256':
            machines = machines.filter(hd_total__range=["117649480", "244277768"])
            title = 'Machines with 256GB Harddisk'

        elif data == '512':
            machines = machines.filter(hd_total__range=["244277769", "975922975"])
            title = 'Machines with 512GB Harddisk'

	elif data == '1024':
            machines = machines.filter(hd_total__gte=975922976)
            title = 'Machines more than 1024GB Harddisk'

        else:
	    machines = None

        return machines, title


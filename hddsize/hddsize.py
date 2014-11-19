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
            t = loader.get_template('thomasbergmann/hddsize/templates/front.html')
	    if not machines:
                machines = utils.getBUmachines(theid)
        if page == 'group_dashboard':
            t = loader.get_template('thomasbergmann/hddsize/templates/front.html')
	    if not machines:
                machine_group = get_object_or_404(MachineGroup, pk=theid)
                machines = Machine.objects.filter(machine_group=machine_group)

	if machines:
	    hdd_size = machines.values('fact__fact_name'='sp_boot_volume').annotate(count=Count('sp_boot_volume')).order_by()
        else:
            hddsize = []

	c = Context({
            'title': 'Disk Size',
	    'data': hdd_size,
            'page': page,
            'theid': theid
        })
        return t.render(c), 4 

    def filter_machines(self, machines, data):
        machines = machines..filter(fact_sp_boot_volume__exact=data)
	title = 'Macs with '+data

        return machines, title


from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManager
from django.template import loader, Context
from django.db.models import Count
from server.models import *
from django.shortcuts import get_object_or_404
import server.utils as utils

class CpuI5(IPlugin):
	def show_widget(self, page, machines=None, theid=None):

		if page == 'front':
			t = loader.get_template('thomasbergmann/cpui5/templates/front.html')
			if not machines:
				machines = Machine.objects.all()

		if page == 'bu_dashboard':
			t = loader.get_template('thomasbergmann/cpui5/templates/id.html')
			if not machines:
				machines = utils.getBUmachines(theid)
				
		if page == 'group_dashboard':
			t = loader.get_template('thomasbergmann/cpui5/templates/id.html')
			if not machines:
				machine_group = get_object_or_404(MachineGroup, pk=theid)
				machines = Machine.objects.filter(machine_group=machine_group)

		if machines:
			cpu_info = machines.filter(cpu_type__contains='i5').values('cpu_speed').annotate(count=Count('cpu_speed')).order_by()
		else:
			cpu_info = []

		if machines:
			count_all = machines.filter(cpu_type__contains='i5').count()
		else:
			count_all = 0

		c = Context({
			'title': 'Intel Core i5',
			'data': cpu_info,
			'count_all': count_all,
			'page': page,
			'theid': theid
		})
		return t.render(c), 4 

	def filter_machines(self, machines, data):
		if data == 'all':
			machines = machines.filter(cpu_type__contains='i5')
			title = 'Macs with Intel Core i5'
		else:
			machines = machines.filter(cpu_type__contains='i5').filter(cpu_speed__exact=data)
			title = 'Macs with Intel Core i5 at '+data

		return machines, title

#the point now is to create a worker that can use instructions.
import boto3
import json
from subprocess import call
from subprocess import check_output
from helper import *

class Worker():

	def __init__(self):
		
		"""
		Connect to AWS s3 download full swarms parameters. Set the file this 
		will be reading from and the file this will be writing too. 
		"""
		self.direc = get_parent()
		self.params = {}
		self.s3 = boto3.resource('s3')
		self.my_id = check_output(['curl', 'http://169.254.169.254/latest/meta-data/instance-id'])
		self.my_id = "".join(map(chr, self.my_id))
		self.sqs = boto3('sqs', region_name='us-east-1')
		self.state = 'running'
		self.progress = 0.0
		self.queue = sele.sqs.get_queue_by_name(QueueName='swarm.fifo')
		self.controller_listener = Thread(target=self.check_in, daemon=True)
		self.controller_listener.start()
		self.s3.Bucket('swarm-instructions').download_file('instructions.txt', self.file_in)

	def check_in(self):
		while True:
			with open('state.txt', 'r') as f:
				self.state = f.read()
				print(self.progress, self.state)
				time.sleep(3)

	def extract(self):
		"""
		Use the file_in from init to extract this workers specific parameters
		from json dictionary based on ec2 instance ids
		"""		
		with open(self.file_in, 'r') as f:
			swarm_params = json.load(f)
		self.params = swarm_params[self.my_id]


	def run(self):
		"""
		Take the params from extract and run whatever operations you want
		on them. Set self.results in this method based on self.params
		"""
		while i < 10000 and self.state != 'exit':
			report(i,size=10000)
			while self.state == 'pause': pass

		pass


	def report(self,i, size = 100):
		"""
		Post to swarm queue my progress and state
		"""
		d = {
		'message': 'working',
		'id': self.my_id,
		'progress': round(i/size,4)}
		self.progress = round(i/size,4)
		response = self.queue.send_message(MessageBody=json.dumps(d), MessageGroupId='json_bots')

	def dump(self):
		"""
		Use the file_out to write the results of this worker to s3.
		"""
		d = {
		'message': 'complete',
		'id': self.my_id,
		'progress': 'None'}
		response = self.queue.send_message(MessageBody=json.dumps(d), MessageGroupId='json_bots')

		




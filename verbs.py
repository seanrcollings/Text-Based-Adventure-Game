class HandleLanguage():
	def check_verb(self, verb, noun, adjective = ""):
		self.verb = verb
		self.noun = noun
		self.adjective = adjective
		scentence_list = [verb, adjective, noun]
		if verb == "buy":
			self.buy(noun)
		elif verb == "take":
			self.take(noun)

	def buy(self, noun):
		pass


	def take(self, noun)






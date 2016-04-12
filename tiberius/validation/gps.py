successful_sentences = 0
# Query for the number of sentences to ensure we get latest data
for i in range(0, self.supported_sentences):
    if self.update():
        successful_sentences += 1
if successful_sentences < self.supported_sentences:
    return False


if self.latitude is not None:
    if self.latitude is str:
        if self.latitude.startswith("00"):
            self.latitude = self.latitude[2:]
            self.latitude = "-" + self.latitude
            if self.debug:
                print self.latitude
    if self.longitude is str:
        if self.longitude.startswith("00"):
            self.longitude = self.longitude[2:]
            self.longitude = "-" + self.longitude
            if self.debug:
                print self.longitude

    if self.latitude is not "":
        self.latitude = float(self.latitude)
        self.latitude /= 100
    else:
        if self.debug:
                print 'No data in latitude'
    if self.longitude is not "":
        self.longitude = float(self.longitude)
        self.longitude /= 100
    else:
        if self.debug:
                print 'No Data in longitude'
return True

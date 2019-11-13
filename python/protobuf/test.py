import person_info_pb2

person = person_info_pb2.Person()
person.name = "ns2250225"
person.tel = "18826400910"

send_messages = person.SerializeToString()
print send_messages

person2 = person_info_pb2.Person()
person2.ParseFromString(send_messages)
print person2.name
print person2.tel

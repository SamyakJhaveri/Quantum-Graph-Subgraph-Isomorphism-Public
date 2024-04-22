def generate_sequence(start, stop):
   sequence_list = []
   i = start
   while (i < stop):
      if (i > start):
         sequence_list.append(',')
      sequence_list.append(i)
      i += 1
   return ''.join(sequence_list)
def sequence(start, stop):
   builder = []
   i = start
   while (i < stop):
      if (i > start):
         builder.append('|')
      builder.append(i)
      i += 1
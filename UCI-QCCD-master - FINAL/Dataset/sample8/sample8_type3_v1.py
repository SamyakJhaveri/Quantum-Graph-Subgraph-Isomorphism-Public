def sequence(start, stop):
   builder = []
   for i in range(start, stop):
      if (i > start):
         builder.append(',')
      builder.append(i)
   return ''.join(builder)

#9 code from saini's paper
def sequence(start, stop):
   builder = []


   i = start
   
   while (i < stop):
      # check condition first
      if (i > start):
         builder.append(',')
      
      builder.append(i)
      i += 1
   
   return ''.join(builder)
from ebookSystem.models import Book

b=Book.objects.get(id=1)
if b.pageCount==None:
	print 'b.pageCount'
print b.pageCount
print b.partCount
from .models import Review, Wine, Cluster, EmpReview, EmpPossibleResigneeReview
from django_pandas.io import read_frame

qs = EmpReview.objects.all()
df = read_frame(qs)
print(list(df.columns))

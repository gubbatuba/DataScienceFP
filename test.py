import matplotlib
# matplotlib.use("TkAgg")
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pickle

def go(a,coun,chem,wells,dates):

	f = pickle.load(file('nice.pickle'))
	# f = Figure(figsize=(10,5), dpi=100)
        # a = f.add_subplot(111)
        # a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

	return f
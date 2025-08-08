import seaborn as sns
import matplotlib.pyplot as plt

def use_theme():
    sns.set_theme(context="talk", style="whitegrid")
    plt.rcParams["figure.dpi"] = 120
    plt.rcParams["savefig.bbox"] = "tight"
    plt.rcParams["axes.titlesize"] = "large"

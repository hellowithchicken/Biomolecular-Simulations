def get_number_string(string):
    import re
    s = [float(s) for s in re.findall(r'-?\d+\.?\d*', string)]
    return s[0]

def read_xvg(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        x = []
        y = []
        for line in lines:
            try:
                x1 = float(line.split()[0])
                y1 = float(line.split()[1])
                x.append(x1)
                y.append(y1)
            except ValueError:
                pass
    return x, y

def get_df(to_read):
    # define locations of files
    k_310_2 =  '/Users/IggyMac/OneDrive - UvA/2020-2021/Biomolecular simulations/Project/Work/Biomolecular-Simulations/310K/2'
    k_310_1 = '/Users/IggyMac/OneDrive - UvA/2020-2021/Biomolecular simulations/Project/Work/Biomolecular-Simulations/310K/1'
    k_400 = '/Users/IggyMac/OneDrive - UvA/2020-2021/Biomolecular simulations/Project/Work/Biomolecular-Simulations/400K'
    base = '/Users/IggyMac/OneDrive - UvA/2020-2021/Biomolecular simulations/Project/Work/Biomolecular-Simulations'
    # read data
    os.chdir(k_310_1)
    x_310_1, y_310_1 = read_xvg(to_read)

    os.chdir(k_310_2)
    x_310_2, y_310_2 = read_xvg(to_read)

    os.chdir(k_400)
    x_400, y_400 = read_xvg(to_read)
    # create data frame and melt
    df_dict = {"x": x_310_1,
          "310K - 1" : y_310_1,
          "310K - 2" : y_310_2,
          "400K" : y_400}

    df = pd.DataFrame(df_dict)
    df = pd.melt(df, id_vars=['x'], value_vars=['310K - 1', '310K - 2', '400K'])
    df.columns = ['Time', 'Simulation', 'value']
    os.chdir(base)
    return df

def plot_joint(data, text_size = 15, xlabel = "Time (ps)", ylabel = "RMSD (nm)"):
    """
    plots a joint plot of selected dataframe
    """
    plt.style.use('ggplot')
    sns.set_palette("twilight")
    plt.rc('xtick', labelsize=text_size) 
    plt.rc('ytick', labelsize=text_size) 

    f, axs = plt.subplots(1,2,
                      figsize=(10,3),
                      sharey=True,
                     gridspec_kw=dict(width_ratios=[3,0.5]))

    sns.lineplot(data = data,
                x = "Time",
                y = "value",
                hue = "Simulation",
                ax = axs[0])


    sns.kdeplot(data = data,
                y = "value",
                hue = "Simulation",
                legend = False,
                ax = axs[1])
    axs[0].set_xlabel(xlabel, size = text_size) 
    axs[0].set_ylabel(ylabel, size = text_size)
    axs[1].set_xlabel("", size = text_size) 
    axs[1].axes.get_xaxis().set_visible(False)
    axs[0].legend(title = "Simulation", fontsize=text_size, title_fontsize=text_size)

    f.tight_layout()
    
def get_mean(df):
    """
    returns mean values from the simulations data frame
    """
    return df.groupby("Simulation")["value"].mean()

def plot_fes(number, text_size = 15, xlabel = "CV (nm)", ylabel = "Bias potential (kj/mol)", with_minima = False, sizex = 6, sizey = 3):
    """ 
    number - metadynamics simulation number
    with_minima - (not)plot the minima points for the last set in metadynamics simulation
    """
    plt.rcParams["figure.figsize"]= sizex, sizey
    plt.rc('xtick', labelsize=text_size) 
    plt.rc('ytick', labelsize=text_size) 
    base = '/Users/IggyMac/OneDrive - UvA/2020-2021/Biomolecular simulations/Project/Work/Biomolecular-Simulations'
    plot = str(number)
    os.chdir(base + "/Metadynamics/" + plot + "/fes_data")
    file_list = os.listdir()
    df_full = pd.DataFrame()
    for file in file_list:
        if "fes" in file:
            number = get_number_string(file)
            x, y = read_xvg(file)
            df_dict = {"Step" : number,
                      "x": x,
                      "y": y}
            df = pd.DataFrame(df_dict)
            df_full = df_full.append(df)
    sns.lineplot(data = df_full,
            x = "x",
            y = "y",
            hue = "Step")
    
    if with_minima:
        filtered = df_full[df_full.Step == 20]
        ind_min = argrelextrema(np.array(filtered["y"]), np.less)
        minima = filtered.iloc[ind_min]
        #sns.scatterplot(data = minima,
        #                x = "x",
        #                y = "y",
        #                s = 150)
        print(minima)
        plt.scatter(minima["x"], minima["y"], s = 100, c = "r")
    
    plt.ylabel(ylabel, fontsize=text_size)
    plt.xlabel(xlabel, fontsize=text_size)
    plt.tight_layout()
    os.chdir(base)
    

def plot_cv(number, text_size = 15, ylabel = "CV (nm)", xlabel = "Time (ps)"):
    """ 
    plot collective variable of metadynamics simulation
    number - metadynamics simulation number 
    """
    plt.rcParams["figure.figsize"]= 6,3
    plt.rc('xtick', labelsize=text_size) 
    plt.rc('ytick', labelsize=text_size) 
    base = '/Users/IggyMac/OneDrive - UvA/2020-2021/Biomolecular simulations/Project/Work/Biomolecular-Simulations'
    plot = str(number)
    x, y = read_xvg(base + "/Metadynamics/" + plot + '/COLVAR')
    plt.ylabel(ylabel, fontsize=text_size)
    plt.xlabel(xlabel, fontsize=text_size)
    plt.plot(x, y)
    plt.tight_layout()
    return x, y
    
    
def plot_joint_cv(number, text_size = 15, ylabel = "CV", xlabel = "Time"):
    """ 
    creates a joint plot of collective variable of metadynamics simulation
    number - metadynamics simulation number 
    """
    plt.rcParams["figure.figsize"]= 6,3
    plt.rc('xtick', labelsize=text_size) 
    plt.rc('ytick', labelsize=text_size) 
    base = '/Users/IggyMac/OneDrive - UvA/2020-2021/Biomolecular simulations/Project/Work/Biomolecular-Simulations'
    plot = str(number)
    x, y = read_xvg(base + "/Metadynamics/" + plot + '/COLVAR')
    
    data = pd.DataFrame({
        "Time": x,
        "value": y
    })

    f, axs = plt.subplots(1,2,
                      figsize=(10,3),
                      sharey=True,
                     gridspec_kw=dict(width_ratios=[3,0.5]))

    sns.lineplot(data = data,
                x = "Time",
                y = "value",
                ax = axs[0])


    sns.kdeplot(data = data,
                y = "value",
                legend = False,
                ax = axs[1])
    axs[0].set_xlabel(xlabel, size = text_size) 
    axs[0].set_ylabel(ylabel, size = text_size)
    axs[1].set_xlabel("", size = text_size) 
    axs[1].axes.get_xaxis().set_visible(False)
def gen_feature_specific_df(df, pivotfeature, feature, sex=None):
    
    from sklearn.preprocessing import LabelBinarizer
    from sklearn_pandas import DataFrameMapper
    
    columns = [(pivotfeature, None), (feature, LabelBinarizer()),('sex', None)]
    mapper = DataFrameMapper(columns, df_out=True)
    
    df = mapper.fit_transform(df.copy())
    cols = df.columns
    rename_map = {}
    for col in cols:
        rename_map[col] = col.replace(feature + "_", "")

    df = df.rename(columns=rename_map)
    if sex is not None:
        df = df[df['sex'] == sex] 
        
    return df

# https://www.shanelynn.ie/bar-plots-in-python-using-pandas-dataframes/
def custom_plot(df, title, gender, color_list=None, figsize=(12,8)):
    
    import math
    from itertools import cycle, islice
    

    stacked_data = df.apply(lambda x: x*100/sum(x), axis=1)
    if color_list is not None:
        my_colors = list(islice(cycle(color_list), None, len(stacked_data)))
    else:
        my_colors = None

    ax = stacked_data.plot(kind='barh',  stacked=True, color=my_colors, figsize=figsize, title= gender + " members")
    ax.legend(ncol=1, loc='center left', bbox_to_anchor=(1.0, 0.5), title=title)
    ax.grid(False) 
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)


    # Reused with changes from https://gist.github.com/jsoma/c61e56819e4ae315ad5d194a630ccb23
    for rect in ax.patches:
        # Find where everything is located
        height = rect.get_height()
        width = rect.get_width()
        x = rect.get_x()
        y = rect.get_y()

        padding = 0.5

        if width >= 5:
            label_text = str(math.ceil(width)) + "%"
        else:
            label_text = ''


        label_x = x + width - padding
        label_y = y + height / 2
        ax.text(label_x, label_y, label_text, ha='right', va='center', color='white', fontsize=12, weight='bold')
    return ax       


def mean_median_mode_plot(df,feature, boxplot=False):
    #https://stackoverflow.com/questions/51417483/mean-median-mode-lines-showing-only-in-last-graph-in-seaborn
    from matplotlib import pyplot as plt
    import pandas as pd
    import seaborn as sns

    mean=df[feature].mean()
    median=df[feature].median()
    mode=df[feature].mode().get_values()[0]
    
    if boxplot:
        f, (ax_box, ax_hist) = plt.subplots(2, sharex=True, gridspec_kw= {"height_ratios": (0.2, 1)})
        sns.boxplot(df[feature], ax=ax_box)
        ax_box.axvline(mean, color='r', linestyle='--')
        ax_box.axvline(median, color='g', linestyle='-')
        ax_box.axvline(mode, color='b', linestyle='-')
    else:    
        f, (ax_box, ax_hist) = plt.subplots(2, sharex=True, gridspec_kw= {"height_ratios": (0, 1)})            
        
    sns.distplot(df[feature], ax=ax_hist)
    ax_hist.axvline(mean, color='r', linestyle='--')
    ax_hist.axvline(median, color='g', linestyle='-')
    ax_hist.axvline(mode, color='b', linestyle='-')

    plt.legend({'Mean':mean,'Median':median,'Mode':mode})

    ax_box.set(xlabel='')
    plt.show()
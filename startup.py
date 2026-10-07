import pandas as pd 
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(layout="wide",page_title="Startup Analysis")

df=pd.read_csv("startup_cleaned.csv")
df["Date"]=pd.to_datetime(df["Date"])
df["Month"]=df["Date"].dt.month_name()
df["Year"]=df["Date"].dt.year

st.sidebar.title("Startup Funding Analysis")

def load_overall_analysis():
    st.title("Overall Analysis")
    # total investment from 2021-2025
    total=round(df["Amount(Crores)"].sum(),2)
    # Max funding on 1 startip
    max_funding=df.groupby("Startup")["Amount(Crores)"].max().sort_values(ascending=False).head(1).values[0]
    # avg funding 
    avg_funding=round(df.groupby("Startup")["Amount(Crores)"].sum().mean(),2)
    # No. of Startups funded
    no_startup=df["Startup"].nunique()

    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.metric("Total Funding from 2021-2025",str(total)+" Cr")
    with col2:
        st.metric("Maximum funding 2021-2025",str(max_funding)+" Cr")
    with col3:
        st.metric("Avg Funding On Startup",str(avg_funding)+"Cr")
    with col4:
        st.metric("No. of Funded Startups",str(no_startup))

    # MoM graph
    

    year_options = ["All Years","2020", "2021", "2022", "2023", "2024", "2025"]
    select_year=st.selectbox("Select Year",year_options)
    st.subheader("Month by Month Funding Graph")
    temp_df=df.groupby(["Year","Month"])["Amount(Crores)"].sum().reset_index()
    temp_df["X-axis"]=temp_df["Month"]+"-"+temp_df["Year"].astype(str)
    temp_df["Year"] = temp_df["Year"].astype(str)

    if select_year != "All Years":
        temp_df = temp_df[temp_df["Year"] == select_year]
    year_options = ["All Years", 2020, 2021, 2022, 2023, 2024, 2025]

    fig3 ,ax3=plt.subplots(figsize=(14, 6))
    ax3.plot(temp_df["X-axis"],temp_df["Amount(Crores)"])
    if select_year == "All Years":
        step = 3
    else:
        step = 1
    ax3.set_xticks(range(0, len(temp_df), step))
    ax3.set_xticklabels(
    temp_df["X-axis"].iloc[::step],
    rotation=45,
    ha="right"
    )
    ax3.set_xlabel("Month")
    ax3.set_ylabel("Investment Amount (Crores)")
    ax3.set_title("Month by Month Investment")
    fig3.tight_layout()
    st.pyplot(fig3)


    st.subheader("No. of startup Funded in Year")

    temp_series=df.groupby("Year")["Startup"].count()
    fig4 ,ax4=plt.subplots(figsize=(8,3))
    ax4.bar(temp_series.index,temp_series.values)
    st.pyplot(fig4)

def startup_overview():
    st.title("Startup Analysis")

    col0,col1=st.columns(2)
    # highest funded startup
    with col0:
        st.metric("Highest Funded Startup (2020-2025)",df.groupby("Startup")["Amount(Crores)"].sum().idxmax()+" (₹9279.18Cr)")
        st.write("")
    col1,col2,col3=st.columns(3)
    # highest funded startup in 2020
    with col1:
        st.metric("Highest Funded Startup in 2020",df[df["Year"]==2020].groupby("Startup")["Amount(Crores)"].sum().idxmax()+" \n(₹5216Cr)")
        st.write("")
    # highest funded startup in 2021
    with col2:
        st.metric("Highest Funded Startup in 2021",df[df["Year"]==2021].groupby("Startup")["Amount(Crores)"].sum().idxmax()+" \n(₹4239Cr)")
        st.write("")
    # highest funded startup in 2022
    with col3:
        st.metric("Highest Funded Startup in 2022",df[df["Year"]==2022].groupby("Startup")["Amount(Crores)"].sum().idxmax()+" \n(₹6926Cr)")
        st.write("")

    col1,col2,col3=st.columns(3)
    # highest funded startup in 2023
    with col1:
        st.metric("Highest Funded Startup in 2023",df[df["Year"]==2023].groupby("Startup")["Amount(Crores)"].sum().idxmax()+" (₹4053Cr)")
        st.write("")
    # highest funded startup in 2024
    with col2:
        st.metric("Highest Funded Startup in 2020",df[df["Year"]==2024].groupby("Startup")["Amount(Crores)"].sum().idxmax()+" \n(₹5403Cr)")
        st.write("")
    # highest funded startup in 2025
    with col3:
        st.metric("Highest Funded Startup in 2020",df[df["Year"]==2025].groupby("Startup")["Amount(Crores)"].sum().idxmax()+" \n(₹4568Cr)")
        st.write("")

    # Year wise Funding
    st.subheader("Year-Wise Funding")
    yearwise_funding=df.groupby("Year")["Amount(Crores)"].sum()
    fig1,ax1=plt.subplots(figsize=(11,4))
    ax1.bar(yearwise_funding.index,yearwise_funding.values)
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Funding Amount(Crores)")
    ax1.set_title("Yearwise Funding")
    st.pyplot(fig1)   
 


def load_startup(startup):

    st.title(startup)
    # Total Funding on startup
    total_funding=round(df.groupby("Startup")["Amount(Crores)"].sum()[startup],2)
    # Avg funding 
    avg_funding=round(df[df["Startup"]==startup]["Amount(Crores)"].mean(),2)
    # Highest funding 
    max_funding=round(df[df["Startup"]==startup]["Amount(Crores)"].max(),2)
    # lowest funding
    min_funding=round(df[df["Startup"]==startup]["Amount(Crores)"].min(),2)
    # No of investor 
    no_of_investor=df[df["Startup"]==startup]["Investors"].str.split(",").explode().str.strip().nunique()
    col1,col2,col3,col4,col0=st.columns(5)
    with col1:
        st.metric("Total Funding",str(total_funding)+"Cr")
    with col2:
        st.metric("Avg Funding",str(avg_funding)+"Cr")
    with col3:
        st.metric("Max Funding",str(max_funding)+"Cr")
    with col4:
        st.metric("Min Funding ",str(min_funding)+"Cr")
    with col0:
        st.metric("No. of Investor ",no_of_investor)


    startup_df=df[df["Startup"]==startup]

    # Startup profile
    st.subheader("Startup Profile")
    col1, col2, col3 = st.columns(3)
    with col1:
        industries = startup_df["Industry"].dropna().unique().tolist()
        st.info("**• Industries**")
        for industry in industries:
            st.write(f" {industry}")
    with col2:
        subverticals = startup_df["SubVertical"].dropna().unique().tolist()
        st.info("**• Sub-Verticals**")
        for subvertical in subverticals:
            st.write(f" {subvertical}")
    with col3:
        cities = startup_df["City"].dropna().unique().tolist()

        st.info("**• Cities**")
        for city in cities:
            st.write(f" {city}")

    st.info("Investor List")
    investors=df[df["Startup"]==startup]["Investors"].str.split(",").explode().str.strip().unique().tolist()

    cols=st.columns(3)

    for i,name in enumerate(investors):
        with cols[i%3]:
            st.write(f"• {name}")

    # Startup funding history
    st.subheader("Funding History")
    funding_history=startup_df.sort_values("Date")
    fig5,ax5=plt.subplots(figsize=(12,5))
    ax5.plot(funding_history["Date"],funding_history["Amount(Crores)"],marker='o')
    ax5.set_xlabel("Date")
    ax5.set_ylabel("Funding Amount(Crores)")
    ax5.set_title("Funding History")
    plt.xticks(rotation=45)
    fig5.tight_layout()
    st.pyplot(fig5)


    # Investment year wise

    st.subheader("Yearwise Funding")
    year_wise=startup_df.groupby("Year")["Amount(Crores)"].sum()
    fig7,ax7=plt.subplots(figsize=(10,5))
    ax7.bar(year_wise.index,year_wise.values)
    ax7.set_xlabel("Year")
    ax7.set_ylabel("Total Funding Amount (Crores)")
    ax7.set_title("Year-wise Funding")
    plt.xticks(rotation=45)
    fig7.tight_layout()
    st.pyplot(fig7)


    # Investment type and funding

    st.subheader("Funding by Investment Type")
    investment_type=startup_df.groupby("InvestmentType")["Amount(Crores)"].sum().sort_values(ascending=True)
    fig6, ax6 = plt.subplots(figsize=(10, 5))
    ax6.bar(investment_type.index,investment_type.values)
    ax6.set_xlabel("Investment Type")
    ax6.set_ylabel("Funding Amount (Crores)")
    ax6.set_title("Funding by Investment Type")
    plt.xticks(rotation=45)
    fig6.tight_layout()
    st.pyplot(fig6)


def investor_overview():
    investor_data = df[["Investors","Amount(Crores)","Startup"]].copy()
    investor_data["Investors"] = investor_data["Investors"].str.split(",")
    investor_data = investor_data.explode("Investors")
    investor_data["Investors"] = investor_data["Investors"].str.strip()
    col1,col2,col3,col4=st.columns(4)
    with col1:
        no_of_investor=df["Investors"].str.split(",").explode().nunique()
        st.metric("Total Investors",str(no_of_investor))
    with col2:
        st.metric("Total Investment",str(round(df["Amount(Crores)"].sum(),2))+"Cr")

    with col3:
        active_investor=investor_data["Investors"].value_counts().head(1).index[0]
        st.metric("Active Investor",active_investor)
    with col4:
        st.metric("Top Investor by Amount",investor_data.groupby("Investors")["Amount(Crores)"].sum().idxmax())

    top_investors = (
    investor_data.groupby("Investors")
    .agg(
        Total_Investment=("Amount(Crores)", "sum"),
        Startups_Invested=("Startup", "nunique")
        ).sort_values("Total_Investment", ascending=False).head(10))
    col1,col2=st.columns(2)
    with col1:
        st.subheader("Top 10 Investors")
        st.dataframe(top_investors)
    with col2:
        st.subheader("Year-wise Investment")
        yearly_investment=df.groupby("Year")["Amount(Crores)"].sum()
        fig1,ax1=plt.subplots()
        ax1.bar(yearly_investment.index,yearly_investment.values)
        ax1.set_xlabel("Year")
        ax1.set_ylabel("Total Investment (Crores)")
        ax1.set_title("Year-wise Investment")
        st.pyplot(fig1)

def load_investor(investor):
    st.title(investor)

    # Recent 5 Investments by the Investor
    latest_investments=df[df["Investors"].str.contains(investor)].sort_values("Date",ascending=False).head()[["Date","Startup","Industry","City","InvestmentType","Amount(Crores)"]].set_index("Date")
    st.subheader("Recent Investments by {}".format(investor))
    st.dataframe(latest_investments)

    col1,col2=st.columns(2)
    with col1:
        # Large amount of Investments 
        
        st.subheader("Biggest Investments by {}".format(investor))
        large_investments=df[df["Investors"].str.contains("Y Combinator")].groupby("Startup")["Amount(Crores)"].sum().sort_values(ascending=False).head()
        # large_investments=df[df["Investors"].str.contains("Y Combinator")].sort_values("Amount(Crores)",ascending=False)[["Startup","Date","InvestmentType","Amount(Crores)"]].set_index("Startup").head(10)
        st.dataframe(large_investments)

    with col2:
        # invest ment in industry
        st.subheader("Investment in Industry")
        investment_industry=df[df["Investors"].str.contains(investor)].groupby("Industry")["Amount(Crores)"].sum()
        fig ,ax=plt.subplots()
        ax.bar(investment_industry.index,investment_industry.values)
        plt.xticks(rotation=90)
        st.pyplot(fig)

    col3,col4=st.columns(2)
    with col3:
        # investment in Cities
        st.subheader("Investment in Cities")
        city_investment=df[df["Investors"].str.contains(investor)].groupby("City")["Amount(Crores)"].sum()
        fig1,ax1=plt.subplots()
        ax1.pie(city_investment,labels=city_investment.index,autopct="%0.01f%%")
        st.pyplot(fig1)

    with col4:
        df["Year"]=df["Date"].dt.year
        st.subheader("Year by Year Investment")
        year_investment=df[df["Investors"].str.contains(investor)].groupby("Year")["Amount(Crores)"].sum()
        fig2,ax2=plt.subplots()
        ax2.plot(year_investment.index,year_investment.values,marker="o")
        st.pyplot(fig2)


option=st.sidebar.selectbox("Select One",["Overall Analysis","Startup","Invester"])

if option == "Overall Analysis":
    load_overall_analysis()

elif option == "Startup":
    selected_startup=st.sidebar.selectbox("Select Startup",sorted(df["Startup"].unique().tolist()))
    butn1=st.sidebar.button("Find Startup Detail")
    if butn1:
        load_startup(selected_startup)
    else:
        startup_overview()
else:
    st.title("Invester Analysis")
    selected_investor=st.sidebar.selectbox("Select Invester",sorted(df["Investors"].str.split(",").explode().str.strip().unique().tolist()))
    butn2=st.sidebar.button("Find Invester Detail")
    if butn2:
        load_investor(selected_investor)
    else:
        investor_overview()

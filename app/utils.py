from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from pymongo import MongoClient
from datetime import datetime
from scipy.stats import pearsonr
import smtplib
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# connect to MongoDB
client = MongoClient('localhost', 27017)
db = client['testdb']
collection = db['testdata']

# initialize the correlation value to 0
corr_value = 0

# function to calculate correlation and send email alert
def calculate_correlation():
    global corr_value
    # get all the data from the collection
    data = pd.DataFrame(list(collection.find()))
    # check if there are more than 2 rows of data
    if data.shape[0] > 2:
        # calculate correlation between SeverityValue and ThreadID
        corr, _ = pearsonr(data['SeverityValue'], data['ThreadID'])
        corr_value = corr
        # if correlation is greater than 0.8, send alert email to the user
        if corr > 0.8:
            sender_email = "sender@example.com"
            receiver_email = "receiver@example.com"
            password = "password"
            message = f"Correlation Alert! Correlation between SeverityValue and ThreadID is {corr_value}"
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message)

# function to plot the line chart
def plot_line_chart():
    # get all the data from the collection
    data = pd.DataFrame(list(collection.find()))
    # convert EventTime to datetime
    data['EventTime'] = pd.to_datetime(data['EventTime'], format='%Y-%m-%d %H:%M:%S')
    # sort data by EventTime
    data.sort_values('EventTime', inplace=True)
    # plot the line chart
    plt.plot(data['EventTime'], data['SeverityValue'])
    plt.xlabel('Event Time')
    plt.ylabel('Severity Value')
    plt.title('Severity Value vs Event Time')
    plt.gcf().autofmt_xdate()
    plt.draw()
    plt.pause(0.001)
    plt.clf()

# function to update the line chart continuously
@require_POST
@csrf_exempt
def update_line_chart(request):
    # update correlation value and plot the line chart
    calculate_correlation()
    plot_line_chart()
    # return empty response
    return HttpResponse()

# function to animate the line chart
def animate(i):
    # clear the plot
    plt.clf()
    # plot the updated line chart
    plot_line_chart()

# initialize the plot figure
fig = plt.figure()

# animate the plot continuously
ani = FuncAnimation(fig, animate, interval=5000)

# render the chart in the webpage
def chart(request):
    return render(request, 'chart.html')

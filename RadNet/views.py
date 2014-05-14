import traceback
from crispy_forms.layout import Submit
from django.contrib.auth.decorators import login_required
from django.forms.models import formset_factory
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
#import sys
#import traceback
#from django.http import HttpResponseRedirect
from django.shortcuts import render
#from calculate import fitToCurve
#from datetime import datetime
import sys
from RadNet.forms import FilterForm, AlphaCoeffForm, BetaCoeffForm, RawDataForm, NumberOfRawData, RawDataFormSetHelper
from RadNet.models import AlphaEfficiency, BetaEfficiency, Filter


def home(request):
    context = RequestContext(request)

    return render_to_response('RadNet/index.html', {}, context)


@login_required
def add_data(request):
    return render(request, 'RadNet/addData.html')


@login_required
def add_filter(request):
    if request.method == 'POST':
        filter_form = FilterForm(request.POST)
        try:
            if filter_form.is_valid():
                filter_form.save()
        except:
            pass
    else:
        filter_form = FilterForm()

    return render(request, 'RadNet/addFilter.html',
                  {'filter_form': filter_form, })


@login_required
def add_coefficients(request, type_id=0):
    if request.method == 'POST' and str(type_id) == str(1):
        alpha_form = AlphaCoeffForm(request.POST)
        if alpha_form.is_valid():
            #AlphaEfficiency.objects.\
                #get(coefficient=alpha_form.cleaned_data['coefficient'])
            alpha_form.save()

        beta_form = BetaCoeffForm()
    elif request.method == 'POST' and str(type_id) == str(2):
        beta_form = BetaCoeffForm(request.POST)
        if beta_form.is_valid():
            #BetaEfficiency.objects.\
                #get(coefficient=beta_form.cleaned_data['coefficient'])
            beta_form.save()

        alpha_form = AlphaCoeffForm()
    else:
        alpha_form = AlphaCoeffForm()
        beta_form = BetaCoeffForm()

    return render(request, 'RadNet/addCoeffs.html',
                  {'alphaForm': alpha_form,
                   'betaForm': beta_form, })


@login_required()
def add_raw_data(request):
    if request.method == 'POST':
        get_number_of_rows = NumberOfRawData(request.POST)
        if get_number_of_rows.is_valid():
            data = get_number_of_rows.cleaned_data
            number_of_rows = int(data['rows'])
            raw_data_form_set = formset_factory(RawDataForm, extra=number_of_rows)
            raw_data_form = raw_data_form_set()
            raw_data_helper = RawDataFormSetHelper()
            raw_data_helper.add_input(Submit("submit", "Save"))
        else:
            raw_data_form = None
            raw_data_helper = None
    else:
        get_number_of_rows = NumberOfRawData()
        raw_data_form = None
        raw_data_helper = None

    return render(request, 'RadNet/addRawData.html',
                  {'getRows': get_number_of_rows, 'rawDataForm': raw_data_form, 'rawHelper': raw_data_helper, })

"""
def checkData(request, filter_id=0):
    if (request.method == 'POST' and filter_id == 0):
        getFilterForm = GetFilterForm(request.POST)
        if getFilterForm.is_valid():
            selection = getFilterForm.cleaned_data['filterID']
            return HttpResponseRedirect('/Data/AddRawData/CheckData/' +
                                        str(selection.id) + '/')
    elif (request.method == 'POST' and filter_id != 0):
        mainFilter = Filter.objects.get(id=filter_id)
        if not mainFilter.activityCalculated:
            rawData = RawData.objects.filter(Filter=filter_id)
            rawData = rawData.order_by('time')
            for data in rawData:
                activity = Activity()
                activity.Filter = mainFilter
                activity.RawData = data
                activity.fillData()
                activity.save()
            mainFilter.activityCalculated = True
            mainFilter.save()
            return HttpResponseRedirect('/Data/FitToCurve/' +
                                        str(filter_id) + '/')
        else:
            HttpResponseRedirect('/Data/ViewData/' + str(filter_id) + '/')
    elif filter_id != 0:
        try:
            mainFilter = Filter.objects.get(id=filter_id)
            if mainFilter.activityCalculated:
                return HttpResponseRedirect('/Data/ViewData/' +
                                            str(filter_id) + '/')
            rawData = RawData.objects.filter(Filter=filter_id)
            rawData = rawData.order_by('time')
            activityData = []
            for data in rawData:
                activity = Activity()
                activity.Filter = mainFilter
                activity.RawData = data
                activity.fillData()
                activityData.append(activity)
            getFilterForm = None
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value,
                                               exc_traceback)
            print ''.join('!! ' + line for line in lines)
            getFilterForm = GetFilterForm()
            filter_id = 0
            mainFilter = None
            activityData = None
    else:
        getFilterForm = GetFilterForm()
        mainFilter = None
        activityData = None
    context = {'getFilterForm': getFilterForm,
               'filter_id': filter_id,
               'mainFilter': mainFilter,
               'activityData': activityData, }
    return render(request, 'Data/checkData.html', context)


def viewData(request, filter_id=0):
    if request.method == 'POST':
        getFilterForm = GetFilterForm(request.POST)
        if getFilterForm.is_valid():
            selection = getFilterForm.cleaned_data['filterID']
            return HttpResponseRedirect('/Data/ViewData/' +
                                        str(selection.id) + '/')
    elif (filter_id != 0):
        try:
            mainFilter = Filter.objects.get(id=filter_id)
            activity = Activity.objects.filter(Filter=filter_id)
            activity = activity.order_by('deltaT')
            getFilterForm = None
        except:
            filter_id = 0
            mainFilter = None
            activity = None
    else:
        mainFilter = None
        activity = None
    getFilterForm = GetFilterForm()
    context = {'getFilterForm': getFilterForm,
               'filter_id': filter_id,
               'activity': activity,
               'mainFilter': mainFilter, }
    return render(request, 'Data/viewData.html', context)


def fitCurve(request, filter_id=0):
    try:
        alphaCurve = AlphaCurve.objects.get(Filter=filter_id)
        betaCurve = BetaCurve.objects.get(Filter=filter_id)
        context = {'alphaCurve': alphaCurve,
                   'betaCurve': betaCurve, }
        return render(request, 'Data/fitCurve.html', context)
    except:
        if filter_id == 0:
            return HttpResponseRedirect('/Data/')
        else:
            fitToCurve(filter_id)
            return HttpResponseRedirect('/Data/FitToCurve/' +
                                        str(filter_id) + '/')


def uploadData(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filterid = uploadDataFromFile(request.FILES['file'])
            if filterid is None:
                filterid = 0
            return HttpResponseRedirect('/Data/AddRawData/CheckData/' +
                                        str(filterid) + '/')
    else:
        form = UploadFileForm()
    return render(request, 'Data/uploadData.html', {'form': form, })


def uploadDataFromFile(fileStuff):
    filterID = None
    with open(fileStuff.name, 'wb+') as destination:
        for chunk in fileStuff.chunks():
            destination.write(chunk)

    with open(fileStuff.name, 'rb') as f:
        try:
            #get initial values
            dataFilterNum = f.readline().rstrip()
            startDate = f.readline().rstrip()
            endDate = f.readline().rstrip()
            sampleTime = f.readline().rstrip()
            sampleVol = f.readline().rstrip()

            for line in f:
                # check if no line if len(line) != 0:
                    # check for comment lines
                    if line[0] != '#':
                        # Check if it's the initial value for time and set it
                        # this part is for the old typed data which didn't
                        # have the calibration numbers in the data textfile
                        if ',' not in line:
                            timeStart = timeToHours(line)
                            alphaCal = 1.63
                            betaCal = 1.15
                        elif len(line.split(',')) == 3:
                            timeStart, alphaCal, betaCal = \
                                line.rstrip().split(',')
                            timeStart = timeToHours(timeStart)
                            alphaCal = float(alphaCal)
                            betaCal = float(betaCal)

                        if ',' not in line or len(line.split(',')) == 3:
                            #check database to see if alphaCal is in already
                            if not AlphaEfficiency.\
                                    objects.filter(coefficient=alphaCal).\
                                    exists():
                                alphaEff = AlphaEfficiency()
                                alphaEff.coefficient = alphaCal
                                alphaEff.save()
                            else:
                                alphaEff = AlphaEfficiency.objects.\
                                    get(coefficient=alphaCal)

                            # check database to see if betaCal is in already
                            if not BetaEfficiency.objects.\
                                    filter(coefficient=betaCal).exists():
                                betaEff = BetaEfficiency()
                                betaEff.coefficient = betaCal
                                betaEff.save()
                            else:
                                betaEff = BetaEfficiency.objects.\
                                    get(coefficient=betaCal)

                            #make new filter entry if it doesn't exists
                            if not Filter.objects.\
                                    filter(filterNum=dataFilterNum).exists():
                                mainFilter = Filter()
                                mainFilter.filterNum = dataFilterNum
                                mainFilter.startDate = \
                                    datetime.strptime(startDate, '%Y%m%d').\
                                    date()
                                mainFilter.endDate = \
                                    datetime.strptime(endDate, '%Y%m%d').date()
                                mainFilter.sampleTime = sampleTime
                                mainFilter.sampleVolume = sampleVol
                                mainFilter.timeStart = timeStart
                                mainFilter.alphaCoeff = alphaEff
                                mainFilter.betaCoeff = betaEff
                                mainFilter.save()
                                mainFilter = Filter.objects.\
                                    get(filterNum=dataFilterNum)
                            else:
                                mainFilter = Filter.objects.\
                                    get(filterNum=dataFilterNum)
                            filterID = mainFilter.id
                        else:
                            #Set the values for each line
                            #det2 is beta+Alpha reading
                            #det1 is alpha reading
                            #cfc is clean filter count
                            time, det2, cfc, det1 = line.rstrip().split(',')
                            rawTime = time
                            det2 = int(det2)
                            cfc = int(cfc)
                            det1 = int(det1)

                            if not RawData.objects.\
                                    filter(Filter=mainFilter, time=rawTime):
                                newRawData = RawData()
                                newRawData.Filter = mainFilter
                                newRawData.time = rawTime
                                newRawData.alphaReading = det1
                                newRawData.betaReading = det2
                                newRawData.cleanFilterCount = cfc
                                newRawData.save()
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type,
                                               exc_value, exc_traceback)
            print ''.join('!! ' + line for line in lines)
    return filterID
"""

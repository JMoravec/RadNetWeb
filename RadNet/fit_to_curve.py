from django.contrib.auth.decorators import login_required

__author__ = 'Joshua Moravec'
import pyeq2
from RadNet.models import Filter, Activity, AlphaCurve, BetaCurve


def fit_to_curve(filter_id):
    equation = pyeq2.Models_2D.Exponential.DoubleExponential()

    #filter_id = int(filter_id)

    #get activity numbers from database
    main_filter = Filter.objects.get(id=filter_id)

    activity = Activity.objects.filter(filter=main_filter).order_by('delta_t')

    # What this section does is reads the data from the file
    # given from the initial argument and formats it so the zunzun.com
    # code can read it.
    # We need two separate Strings so we can have two equations found.
    alpha = 'X\tY\n'
    beta = 'X\tY\n'

    # set the stings with the data points from the database
    for data_point in activity:
        alpha = alpha + str(data_point.delta_t) + "\t" + str(data_point.alpha_activity) + "\n"
        beta = beta + str(data_point.delta_t) + "\t" + str(data_point.beta_activity) + "\n"

    #fit plot to alpha data
    #get coefficients from zunzun
    data = alpha
    pyeq2.dataConvertorService().ConvertAndSortColumnarASCII(data, equation, False)
    equation.Solve()

    #change the coefficients to float type
    alpha_initial_1 = float(equation.solvedCoefficients[0])
    alpha_lam_1 = float(equation.solvedCoefficients[1])
    alpha_initial_2 = float(equation.solvedCoefficients[2])
    alpha_lam_2 = float(equation.solvedCoefficients[3])

    # put data into database
    new_curve_a = AlphaCurve()
    new_curve_a.filter = main_filter
    new_curve_a.alpha_1 = alpha_initial_1
    new_curve_a.alpha_2 = alpha_initial_2
    new_curve_a.alpha_1_lambda = alpha_lam_1
    new_curve_a.alpha_2_lambda = alpha_lam_2

    #try to save
    new_curve_a.save()

    #fit plot to beta data
    data = beta
    pyeq2.dataConvertorService().ConvertAndSortColumnarASCII(data, equation, False)
    equation.Solve()

    beta_initial_1 = float(equation.solvedCoefficients[0])
    beta_lam_1 = float(equation.solvedCoefficients[1])
    beta_initial_2 = float(equation.solvedCoefficients[2])
    beta_lam_2 = float(equation.solvedCoefficients[3])

    new_curve_b = BetaCurve()
    new_curve_b.filter = main_filter
    new_curve_b.beta_1 = beta_initial_1
    new_curve_b.beta_2 = beta_initial_2
    new_curve_b.beta_1_lambda = beta_lam_1
    new_curve_b.beta_2_lambda = beta_lam_2
    new_curve_b.save()
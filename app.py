from flask import Flask, request
import joblib
import numpy

MODEL_PATH = 'mlmodels/model.pkl'
SCALER_X_PATH = 'mlmodels/scaler_x.pkl'
SCALER_Y_PATH = 'mlmodels/scaler_y.pkl'

MODEL_PATH_ADD = 'mlmodels/model_add.pkl'
SCALER_X_PATH_ADD = 'mlmodels/scaler_x_add.pkl'
SCALER_Y_PATH_ADD = 'mlmodels/scaler_y_add.pkl'

app = Flask(__name__)
model = joblib.load(MODEL_PATH)
sc_x = joblib.load(SCALER_X_PATH)
sc_y = joblib.load(SCALER_Y_PATH)

model_add = joblib.load(MODEL_PATH_ADD)
sc_x_add = joblib.load(SCALER_X_PATH_ADD)
sc_y_add = joblib.load(SCALER_Y_PATH_ADD)


@app.route('/predict_price', methods=['GET'])
def predict():
    args = request.args
    model_version = args.get('model_version', default=1, type=int)
    floor = args.get('floor', default=-1, type=int)
    open_plan = args.get('open_plan', default=-1, type=int)
    rooms = args.get('rooms', default=-1, type=int)
    studio = args.get('studio', default=-1, type=int)
    area = args.get('area', default=-1, type=float)
    kitchen_area = args.get('kitchen_area', default=-1, type=float)
    living_area = args.get('living_area', default=-1, type=float)
    agent_fee = args.get('agent_fee', default=-1, type=float)
    renovation = args.get('renovation', default=-1, type=float)
    days_of_exposition = args.get('days_of_exposition', default=-1, type=int)

    if model_version == 1:
        required_parameters = [open_plan, rooms, studio, area, \
                               kitchen_area, living_area, agent_fee, days_of_exposition]

        if any([param == -1 for param in required_parameters]):
            return '500 Internal server error'

        x = numpy.array([open_plan, rooms, studio, area, kitchen_area, \
                         living_area, agent_fee, days_of_exposition]).reshape(1, -1)
        x = sc_x.transform(x)
        result = model.predict(x)
        result = sc_y.inverse_transform(result.reshape(1, -1))

        return str(result[0][0])

    elif model_version == 2:
        required_parameters_add = [floor, open_plan, rooms, studio, area, \
                                   kitchen_area, living_area, agent_fee, renovation, days_of_exposition]

        if any([param == -1 for param in required_parameters_add]):
            return '500 Internal server error'

        x = numpy.array([floor, open_plan, rooms, studio, area, kitchen_area, \
                         living_area, agent_fee, renovation, days_of_exposition]).reshape(1, -1)
        x = sc_x_add.transform(x)
        result = model_add.predict(x)
        result = sc_y_add.inverse_transform(result.reshape(1, -1))

        return str(result[0][0])

    else:
        return '500 Internal server error'


if __name__ == '__main__':
    app.run(debug=True, port=4444, host='0.0.0.0')

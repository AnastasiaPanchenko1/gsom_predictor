from flask import Flask, request
import joblib
import numpy
MODEL_PATH = 'mlmodels/model.pkl'
SCALER_X_PATH = 'mlmodels/scaler_x.pkl'
SCALER_Y_PATH = 'mlmodels/scaler_y.pkl'

app = Flask(__name__)
model = joblib.load(MODEL_PATH)
sc_x = joblib.load(SCALER_X_PATH)
sc_y = joblib.load(SCALER_Y_PATH)
@app.route("/predict_price", methods = ['GET'])
def predict():
    args = request.args
    open_plan = args.get('open_plan', default=-1, type=int)
    rooms = args.get('rooms', default=-1, type=int)
    studio = args.get('studio', default=-1, type=int)
    area = args.get('area', default=-1, type=float)
    kitchen_area = args.get('kitchen_area', default=-1, type=float)
    living_area = args.get('living_area', default=-1, type=float)
    agent_fee = args.get('agent_fee', default=-1, type=float)
    days_of_exposition = args.get('days_of_exposition', default= -1, type=int)

    # response = "open_plan:{}, rooms:{}, studio:{}, area:{}, kitchen_area: {}, living_area:{}, agent_fee:{}, days_of_exposition:{}".format(open_plan, rooms, studio, area, kitchen_area, living_area, agent_fee, days_of_exposition)


    x = numpy.array([open_plan, rooms, studio, area, kitchen_area, living_area, agent_fee, days_of_exposition]).reshape(1,-1)
    x = sc_x.transform(x)
    result = model.predict(x)
    result = sc_y.inverse_transform(result.reshape(1,-1))

    return str(result[0][0])


if __name__ == '__main__':
    app.run(debug=True, port=5444, host='0.0.0.0')
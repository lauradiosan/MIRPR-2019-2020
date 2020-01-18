package org.tensorflow.lite.examples.detection.http;

import java.util.List;

import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Query;

public interface WeatherService {

    @GET("currentconditions/v1/287713")
    Call<List<WeatherResponse>> getCurrentWeather(@Query("apikey") String apiKey);
}

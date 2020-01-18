package org.tensorflow.lite.examples.detection.http;

import okhttp3.OkHttpClient;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class RetrofitFactory {
    private static Retrofit retrofit = null;
    private static OkHttpClient okHttpClient = null;

    public RetrofitFactory() {
    }

    public static Retrofit getRetrofit() {
        if (okHttpClient == null) {
            okHttpClient = new OkHttpClient.Builder()
                    .build();
        }

        if (retrofit == null) {
            retrofit = new Retrofit.Builder()
                    .baseUrl("http://dataservice.accuweather.com")
                    .addConverterFactory(GsonConverterFactory.create())
                    .client(okHttpClient)
                    .build();
        }
        return retrofit;
    }
}

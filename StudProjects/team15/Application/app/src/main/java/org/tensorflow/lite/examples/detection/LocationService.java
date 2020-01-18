//package org.tensorflow.lite.examples.detection;
//
//import android.annotation.SuppressLint;
//import android.app.Service;
//import android.content.Intent;
//import android.location.Location;
//import android.location.LocationListener;
//import android.os.Binder;
//import android.os.Bundle;
//import android.os.IBinder;
//
//import androidx.annotation.Nullable;
//
//import com.google.android.gms.common.ConnectionResult;
//import com.google.android.gms.common.api.GoogleApiClient;
//import com.google.android.gms.location.LocationRequest;
//import com.google.android.gms.location.LocationServices;
//
//import java.text.DecimalFormat;
//import java.util.concurrent.TimeUnit;
//
///**
// * Created by vipul on 12/13/2015.
// */
//public class LocationService extends Service implements
//        LocationListener,
//        GoogleApiClient.ConnectionCallbacks,
//        GoogleApiClient.OnConnectionFailedListener {
//
//    private static final long INTERVAL = 1000 * 2;
//    private static final long FASTEST_INTERVAL = 1000 * 1;
//    LocationRequest mLocationRequest;
//    GoogleApiClient mGoogleApiClient;
//    Location mCurrentLocation, lStart, lEnd;
//    static double distance = 0;
//    double speed;
//
//
//    private final IBinder mBinder = new LocalBinder();
//
//    @Nullable
//    @Override
//    public IBinder onBind(Intent intent) {
//        createLocationRequest();
//        mGoogleApiClient = new GoogleApiClient.Builder(this)
//                .addApi(LocationServices.API)
//                .addConnectionCallbacks(this)
//                .addOnConnectionFailedListener(this)
//                .build();
//        mGoogleApiClient.connect();
//        return mBinder;
//    }
//
//    @SuppressLint("RestrictedApi")
//    protected void createLocationRequest() {
//        mLocationRequest = new LocationRequest();
//        mLocationRequest.setInterval(INTERVAL);
//        mLocationRequest.setFastestInterval(FASTEST_INTERVAL);
//        mLocationRequest.setPriority(LocationRequest.PRIORITY_HIGH_ACCURACY);
//    }
//
//
//    @Override
//    public int onStartCommand(Intent intent, int flags, int startId) {
//
//        return super.onStartCommand(intent, flags, startId);
//    }
//
//
//    @Override
//    public void onConnected(Bundle bundle) {
//        try {
//            LocationServices.FusedLocationApi.requestLocationUpdates(
//                    mGoogleApiClient, mLocationRequest, (com.google.android.gms.location.LocationListener) this);
//        } catch (SecurityException e) {
//        }
//    }
//
//
//    protected void stopLocationUpdates() {
//        LocationServices.FusedLocationApi.removeLocationUpdates(
//                mGoogleApiClient, (com.google.android.gms.location.LocationListener) this);
//        distance = 0;
//    }
//
//
//    @Override
//    public void onConnectionSuspended(int i) {
//
//    }
//
//
//    @Override
//    public void onLocationChanged(Location location) {
////        CameraActivity.locate.dismiss();
//        mCurrentLocation = location;
//        if (lStart == null) {
//            lStart = mCurrentLocation;
//            lEnd = mCurrentLocation;
//        } else
//            lEnd = mCurrentLocation;
//
//        //Calling the method below updates the  live values of distance and speed to the TextViews.
//        updateUI();
//        //calculating the speed with getSpeed method it returns speed in m/s so we are converting it into kmph
//        speed = location.getSpeed() * 18 / 5;
//
//    }
//
//    @Override
//    public void onStatusChanged(String s, int i, Bundle bundle) {
//
//    }
//
//    @Override
//    public void onProviderEnabled(String s) {
//
//    }
//
//    @Override
//    public void onProviderDisabled(String s) {
//
//    }
//
//    @Override
//    public void onConnectionFailed(ConnectionResult connectionResult) {
//
//    }
//
//    public class LocalBinder extends Binder {
//
//        public LocationService getService() {
//            return LocationService.this;
//        }
//
//
//    }
//
//    //The live feed of Distance and Speed are being set in the method below .
//    private void updateUI() {
//            distance = distance + (lStart.distanceTo(lEnd) / 1000.00);
//            if (speed > 0.0)
//                CameraActivity.speed.setText("Current speed: " + new DecimalFormat("#.##").format(speed) + " km/hr");
//            else
//                CameraActivity.speed.setText(".......");
//
//            lStart = lEnd;
//    }
//
//
//    @Override
//    public boolean onUnbind(Intent intent) {
//        stopLocationUpdates();
//        if (mGoogleApiClient.isConnected())
//            mGoogleApiClient.disconnect();
//        lStart = null;
//        lEnd = null;
//        distance = 0;
//        return super.onUnbind(intent);
//    }
//}
import scr.SensorModel;

public class CarState {
	
	private double changeDistanceFromStartLine = 0;
	private double lastDistanceFromStartLine=0 ;
	
	private double changeAngleToTrackAxis = 0;
	private double lastAngleToTrackAxis = 0 ;
	
	private double changeSpeed = 0;
	private double lastSpeed = 0 ;
	 
	
	private SensorModel sensors;
	/**
	   * Updates the state with the given Environment.
	   */
	  
	public void update(SensorModel sensors) {
		this.sensors = sensors;
		changeDistanceFromStartLine = sensors.getDistanceFromStartLine() - lastDistanceFromStartLine;
		lastDistanceFromStartLine = sensors.getDistanceFromStartLine();
		
		changeAngleToTrackAxis = sensors.getAngleToTrackAxis() - lastAngleToTrackAxis;
		lastAngleToTrackAxis = sensors.getAngleToTrackAxis();
		
		changeSpeed = sensors.getSpeed() - lastSpeed;
		lastSpeed = sensors.getSpeed();
	
	}
	
	public float calculateReward() {
		float re = 0;
		 re += this.changeSpeed;
//		 re += this.changeAngleToTrackAxis;
		 re += this.changeDistanceFromStartLine;
		 
		 re += (-sensors.getTrackPosition());
		 
		
		return re;
	}

	public long getStateNumber() {
		// TODO Auto-generated method stub
		
		int num = (int) (sensors.getAngleToTrackAxis()*10);
		return num;
	}
	  

}

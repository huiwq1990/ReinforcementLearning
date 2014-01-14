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
//		 re += this.changeSpeed;
//		 re += this.changeAngleToTrackAxis;
		 re += this.changeDistanceFromStartLine;
//		 re += this.changeAngleToTrackAxis*4;
//		 re += (-sensors.getTrackPosition())*10;
		 
		float angleToTrackRe = 0;	
		if(-Math.PI/3 < sensors.getAngleToTrackAxis() && sensors.getAngleToTrackAxis()< Math.PI/3){
//			angleToTrackRe = (float) Math.exp(-Math.abs(sensors.getAngleToTrackAxis()))*10 ;
			angleToTrackRe = (float) Math.exp(-Math.abs(sensors.getAngleToTrackAxis()))*10 ;
		}else{
			angleToTrackRe = (float) (-100 * Math.abs(sensors.getAngleToTrackAxis()));	
		}
		
		float trackPosRe = 0;
		
		
		if(-0.75 < sensors.getTrackPosition() && sensors.getTrackPosition() < 0.5 ){
			trackPosRe = (float) Math.exp(-Math.abs(sensors.getTrackPosition()+0.25))*10;
		}else{
			trackPosRe = (float) (-50 * Math.abs(sensors.getTrackPosition()));
		}
		re += angleToTrackRe;
		re += trackPosRe ;
		return re;
	}

	public long getStateNumber() {
		// TODO Auto-generated method stub
		
		int trac = (int) ((sensors.getAngleToTrackAxis() + Math.PI)/(2*Math.PI) * 99);
		
		
//		int pos = 0;
//		if(sensors.getTrackPosition() > 1 ){
//			pos = 0;
//		}else if(sensors.getTrackPosition() < -1 ){
//			pos = 9;
//		}else{
//			pos = (int) (-(sensors.getTrackPosition() - 1)/2.0 *9) ;
//		}
		
		
		int pos =  (int) (-(sensors.getTrackPosition() - TorcsInfo.trackmaxwidth)/(2.0*TorcsInfo.trackmaxwidth) *99) ;
		
		System.out.println(pos);
//		sensors.getAngleToTrackAxis()/Math.PI+1
		
		int num = trac*100 + pos;
		return num;
	}
	  

}

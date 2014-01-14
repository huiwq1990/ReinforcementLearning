import scr.Action;


public class CarAction {
	 
	  // Update the total number when adding new actions.
	  public static final int TOTAL_ACTIONS = 5;
	  
//	  public st
	  
//	  private final int actionNumber;
//	  private final boolean[] action;
	
	  
	  private static double[] steeringArray = {-0.5,-0.2,0,0.2,0.5};
//	  
//	  public int getActionNumber() {
//	    return actionNumber;
//	  }
//	  
//	  public boolean[] getAction() {
//	    return action;
//	  }
	  
	  public static Action getAction(int actionNumber) {
		  Action a = new Action();
		  a.accelerate = 0.3;
//		  a.brake = 0.1;
//		  a.clutch = 0.1;
		  a.gear = 3;
		  a.steering = steeringArray[actionNumber];
	  	 return a;
	  }
	  
	  
//	  public CarAction(int actionNumber, int... keys) {
//		    this.actionNumber = actionNumber;
//		    
//		    this.action = new boolean[6];
//		    for (int key : keys) {
//		      this.action[key] = true;
//		    }
//	 } 
	  
	  
	  public static void main(String[] args) {

		  System.out.println(MarioAction.getAction(2));
	  }
	

}

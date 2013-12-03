package hg.rl;

import pacman.game.Constants.MOVE;

public enum PacManAction {
	

	
	  // Update the total number when adding new actions.
	  public static final int TOTAL_ACTIONS = 12;
	  
	  private final int actionNumber;
	  private final boolean[] action;
	  
	UP(0),	
//	RIGHT(1,MOVE),
//	DOWN(0,MOVE.UP),	
//	LEFT(0,MOVE.UP),	
//	NEUTRAL(0,MOVE.UP),	
	
	 
	//这种声明方式，表示可以多种方式传参，可以为空，可以传一个，可以传多个
//	PacManAction(int actionNumber,MOVE... move) {
//		  
//	
//	}
	PacManAction(int actionNumber) {
		  
		
	}	 
}

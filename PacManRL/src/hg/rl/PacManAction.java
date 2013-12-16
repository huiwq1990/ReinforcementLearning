package hg.rl;

import pacman.game.Constants.MOVE;

public enum PacManAction {

	UP(0,MOVE.UP),
	RIGHT(1,MOVE.RIGHT),
	DOWN(2,MOVE.DOWN),	
	LEFT(3,MOVE.LEFT),
	NEUTRAL(4,MOVE.NEUTRAL);	

	  // Update the total number when adding new actions.
	  public static final int TOTAL_ACTIONS = 5;
	  private final int actionNumber;
	  private final MOVE action;
	  private PacManAction(int actionNumber,MOVE move ) {
		 this.actionNumber = actionNumber;
		 this.action = move;
	  }
	public int getActionNumber() {
		return actionNumber;
	}
	
	
	 public MOVE getAction() {
		return action;
	}
	public static MOVE getAction(int actionNumber) {
		    return PacManAction.values()[actionNumber].getAction();
		  }
	  
	 public static void main(String[] args) {

		  System.out.println(PacManAction.getAction(2));
	  }
}

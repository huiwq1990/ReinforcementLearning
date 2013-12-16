package hg.rl;

import pacman.game.Game;

public class PacManState {
	
	Game game;
	 private long stateNumber = 0;
	
	 /**
	   * Updates the state with the given Environment.
	   */
	  public void update(Game game) {

	    this.game = game;
	    
	  }
	
	
	

	public Game getGame() {
		return game;
	}




	public void setGame(Game game) {
		this.game = game;
	}




	public long getStateNumber() {
		return stateNumber;
	}




	public void setStateNumber(long stateNumber) {
		this.stateNumber = stateNumber;
	}




	public static void main(String[] args) {
		// TODO Auto-generated method stub

	}

}

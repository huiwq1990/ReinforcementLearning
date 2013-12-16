package hg.rl;

import pacman.controllers.Controller;
import pacman.game.Constants.MOVE;
import pacman.game.Game;

public class PacManRLAgent  extends Controller<MOVE>{
	 // Fields for the Mario Agent
	  private PacManState currentState;

	  // Associated Qtable for the agent. Used for RL training.
	  private ActionQtable actionTable;

	  public PacManRLAgent() {
//		    setName("Super Mario 229");
		    
		    currentState = new PacManState();
		    actionTable = new ActionQtable(PacManAction.TOTAL_ACTIONS);
		    
		    if (LearningParams.LOAD_QTABLE) {
		      actionTable.loadQtable(LearningParams.FINAL_QTABLE_NAME);
		    }
		
		  }
	@Override
	public MOVE getMove(Game game, long timeDue) {
		this.currentState.update(game);
		 int actionNumber = actionTable.getNextAction(currentState.getStateNumber());
		    
		    Logger.println(2, "Next action: " + actionNumber + "\n");
		    
		    return PacManAction.getAction(actionNumber);
	}
	
	
	
	
	
	
	  private void learnOnce() {
		    Logger.println(1, "================================================");
		    Logger.println(0, "Trial: %d", learningTrial);

		    init();
		    learningTask.runSingleEpisode(1);

		    EvaluationInfo evaluationInfo =
		        learningTask.getEnvironment().getEvaluationInfo();
		    
		    int score = evaluationInfo.computeWeightedFitness();
		    
		    Logger.println(1, "Intermediate SCORE = " + score);
		    Logger.println(1, evaluationInfo.toStringSingleLine());
		    
		    scores.add(score);

		    // Dump the info of the most visited states into file.
		    if (LearningParams.DUMP_INTERMEDIATE_QTABLE) {
		      actionTable.dumpQtable(
		          String.format(LearningParams.QTABLE_NAME_FORMAT, learningTrial));
		    }
		    
		    learningTrial++;
		  }

		  @Override
		  public void learn() {
		    for (int m = 0; m < LearningParams.NUM_MODES_TO_TRAIN; m++) {
		      options.setMarioMode(m);
		      for (int j = 0; j < LearningParams.NUM_SEEDS_TO_TRAIN; j++) {
		        if (j > 0) {
		          options.setLevelRandSeed(Utils.getSeed(j - 1));
		        }
		        for (int i = 0; i < LearningParams.NUM_TRAINING_ITERATIONS; i++) {
		          learnOnce();
		        }
		      }
		    }
		    setUpForEval();
		  }
	
	
}

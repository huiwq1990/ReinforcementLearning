

import java.util.ArrayList;
import java.util.List;

import scr.Action;
import scr.Controller;
import scr.SensorModel;


public class RLController extends Controller {
	
	private static final int MAX_STEPS = 8000; // about 2?minute
	
	private boolean finished = false;
	
	private int curStep = 0;
	private int curGene = 0;
	 
	  // Fields for the Mario Agent
	  private CarState currentState;

	  // Associated Qtable for the agent. Used for RL training.
	  private ActionQtable actionTable;
	
	public RLController(){
	    currentState = new CarState();
	    actionTable = new ActionQtable(CarAction.TOTAL_ACTIONS);
	}
	
	@Override
	public Action control(SensorModel sensors) {
		 currentState.update(sensors);
		 actionTable.updateQvalue(
		          currentState.calculateReward(), currentState.getStateNumber());
		  // Transforms the best action number to action array.
	    int actionNumber = actionTable.getNextAction(currentState.getStateNumber());
	    
	    Logger.println(2, "Next action: " + actionNumber + "\n");
	    return new Action();
//	    return CarAction.getAction(actionNumber);
	}
	
	

	  private void learnOnce() {
//	    Logger.println(1, "================================================");
//	    Logger.println(0, "Trial: %d", learningTrial);
//
//	    init();
//	   System.out.println( ((MarioRLAgent)learningTask.getAgent()).learningTrial);
//	    learningTask.runSingleEpisode(1);
//
//	    EvaluationInfo evaluationInfo =
//	        learningTask.getEnvironment().getEvaluationInfo();
//	    
//	    int score = evaluationInfo.computeWeightedFitness();
//	    
//	    Logger.println(1, "Intermediate SCORE = " + score);
//	    Logger.println(1, evaluationInfo.toStringSingleLine());
//	    
//	    scores.add(score);
//
//	    // Dump the info of the most visited states into file.
//	    if (LearningParams.DUMP_INTERMEDIATE_QTABLE) {
//	      actionTable.dumpQtable(
//	          String.format(LearningParams.QTABLE_NAME_FORMAT, learningTrial));
//	    }
//	    
//	    learningTrial++;
	  }

//	  @Override
	  public void learn() {
//	    for (int m = 0; m < LearningParams.NUM_MODES_TO_TRAIN; m++) {
//	      options.setMarioMode(m);
//	      for (int j = 0; j < LearningParams.NUM_SEEDS_TO_TRAIN; j++) {
//	        if (j > 0) {
//	          options.setLevelRandSeed(Utils.getSeed(j - 1));
//	        }
//	        for (int i = 0; i < LearningParams.NUM_TRAINING_ITERATIONS; i++) {
//	          learnOnce();
//	        }
//	      }
//	    }
//	    setUpForEval();
	  }


	@Override
	public void reset() {
		//System.out.println(">> Reset call received");
	}

	@Override
	public void shutdown() { }

}

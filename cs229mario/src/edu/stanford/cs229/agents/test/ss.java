package edu.stanford.cs229.agents.test;

import edu.stanford.cs229.agents.Evaluation.Mode;

public class ss {
	  public static enum Mode {
		    DEBUG,
		    DEMO,
		    EVAL;
		    
		    static Mode getMode(String mode) {
		      for (Mode m : Mode.values()) {
		        if (m.name().equalsIgnoreCase(mode)) {
		          return m;
		        }
		      }
		      return Mode.DEMO;
		    }
		  }
	  
	  public static void main(String[] args){
		  System.out.println(Mode.getMode("demo"));
	  }
}

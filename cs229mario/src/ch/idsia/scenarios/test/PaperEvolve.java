/*
 * Copyright (c) 2009-2010, Sergey Karakovskiy and Julian Togelius
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *  Redistributions of source code must retain the above copyright
 * notice, this list of conditions and the following disclaimer.
 *  Redistributions in binary form must reproduce the above copyright
 * notice, this list of conditions and the following disclaimer in the
 * documentation and/or other materials provided with the distribution.
 *  Neither the name of the Mario AI nor the
 * names of its contributors may be used to endorse or promote products
 * derived from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 * IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
 * INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 * NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 * PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 * WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */

package ch.idsia.scenarios.test;

import ch.idsia.agents.Agent;
import ch.idsia.agents.learning.MediumSRNAgent;
import ch.idsia.benchmark.mario.engine.GlobalOptions;
import ch.idsia.benchmark.tasks.ProgressTask;
import ch.idsia.evolution.Evolvable;
import ch.idsia.evolution.ea.ES;
import ch.idsia.tools.MarioAIOptions;
import ch.idsia.utils.statistics.Stats;
import ch.idsia.utils.wox.serial.Easy;

import java.io.IOException;
import java.text.DecimalFormat;

/**
 * Created by IntelliJ IDEA.
 * User: julian
 * Date: Jun 13, 2009
 * Time: 2:16:18 PM
 */
public class PaperEvolve
{
final static int generations = 5000;
final static int populationSize = 100;

public static void main(String[] args)
{
    MarioAIOptions options = new MarioAIOptions(args);
//        Evolvable initial = new LargeSRNAgent();
//        Evolvable initial = new SmallSRNAgent();
//        Evolvable initial = new MediumSRNAgent();
//        Evolvable initial = new SmallMLPAgent();
    Evolvable initial = new MediumSRNAgent();
//        Evolvable initial = new MediumMLPAgent();
//        if (args.length > 0)
//        {
//            initial = (Evolvable) AgentsPool.loadAgent (args[0]);
//        }
    options.setTimeLimit(100);
    options.setAgent((Agent) initial);
    options.setFPS(GlobalOptions.MaxFPS);
    options.setVisualization(false);
    ProgressTask task = new ProgressTask(options);
//        MultiSeedProgressTask task = new MultiSeedProgressTask(options);
//        MushroomTask task = new MushroomTask(options);
    options.setLevelRandSeed(6189642);
//        int seed = (int) (Math.random () * Integer.MAX_VALUE / 100000);
    int seed = options.getLevelRandSeed();
    ES es = new ES(task, initial, populationSize);
    System.out.println("Evolving " + initial + " with task " + task);
//        int difficulty = 0;
//        System.out.println("seed = " + seed);
//        task.uid = seed;

//        options.setLevelRandSeed(seed);
//        BasicTask bt = new MultiSeedProgressTask(new MarioAIOptions(args));
//        MarioAIOptions c = new MarioAIOptions(new String[]{"-vis", "on", "-fps", "24"});

    // start learning in mode 0
//    System.out.println("options.getTimeLimit() = " + options.getTimeLimit());
//        options.setMarioMode(0);
    String fileName = "evolved-" + "-uid-" + seed + ".xml";
    DecimalFormat df = new DecimalFormat();
    float bestScore = 250;

    //options.setLevelDifficulty(16);

    for (int gen = 0; gen < generations; gen++)
    {
//            System.out.print("<a = " + options.getMarioMode() + "> ");
//            task.setStartingSeed(gen);
        es.nextGeneration();

        float fitn = es.getBestFitnesses()[0];
        System.out.print("Generation: " + gen + " current best: " + df.format(fitn) + ";  ");
//            int marioStatus = task.getEnvironment().getEvaluationInfo().marioStatus;

        if (fitn > bestScore /*&& marioStatus == Environment.MARIO_STATUS_WIN*/)
        {
            bestScore = fitn;
            fileName = "evolved-progress-" + options.getAgentFullLoadName() + gen + "-uid-" + seed + ".xml";
            final Agent a = (Agent) es.getBests()[0];
            Easy.save(a, fileName);
            task.dumpFitnessEvaluation(bestScore, "fitnessImprovements-" + options.getAgentFullLoadName() + ".txt");
//                c.setLevelRandSeed(options.getLevelRandSeed());
//                c.setLevelDifficulty(options.getLevelDifficulty());
//                c.setTimeLimit(options.getTimeLimit());
            options.setAgent(a);
            System.out.println("a = " + options.getMarioMode());
//                task.setAgent(a);
            options.setVisualization(true);
            options.setFPS(42);
            task.getEnvironment().reset(options);
            task.evaluate(a);
            options.setVisualization(false);
            options.setFPS(100);

            System.out.print("MODE: = " + task.getEnvironment().getEvaluationInfo().marioMode);
            System.out.print("TIME LEFT: " + task.getEnvironment().getEvaluationInfo().timeLeft);
            System.out.println(", STATUS = " + task.getEnvironment().getEvaluationInfo().marioStatus);

//                difficulty++;
//                options.setLevelDifficulty(difficulty);
        }
    }

    System.out.println("\n\n\n\n\n\n\n\n\n");
    try
    {
        Stats.main(new String[]{fileName, "0"});
    } catch (IOException e)
    {
        e.printStackTrace();
    }
    System.exit(0);
}
}

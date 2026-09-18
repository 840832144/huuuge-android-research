// Ghidra headless postScript —— 反编译匹配的函数并把伪代码落盘
// 用法: -postScript DecompileByRegex.java <关键字...> <outdir> [max]
// 参数约定：以路径分隔符/盘符开头的参数当作输出目录，纯数字当上限，其余当关键字。
// （Ghidra 会把参数按逗号与空格切开，所以不要用逗号或 | 拼关键字。）
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionIterator;

import java.io.File;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;

public class DecompileByRegex extends GhidraScript {

    @Override
    public void run() throws Exception {
        List<String> keys = new ArrayList<>();
        String outdir = ".";
        int max = 20;

        for (String a : getScriptArgs()) {
            String t = a.trim();
            if (t.isEmpty()) {
                continue;
            }
            if (t.matches("\\d+")) {
                max = Integer.parseInt(t);
            } else if (t.contains(":\\") || t.contains("/") || t.contains("\\")) {
                outdir = t;
            } else {
                keys.add(t);
            }
        }

        File dir = new File(outdir);
        if (!dir.isDirectory()) {
            dir.mkdirs();
        }

        DecompInterface dec = new DecompInterface();
        dec.openProgram(currentProgram);

        println("[*] program : " + currentProgram.getName());
        println("[*] keys    : " + keys);
        println("[*] outdir  : " + dir.getAbsolutePath());
        println("[*] max     : " + max);

        FunctionIterator it = currentProgram.getFunctionManager().getFunctions(true);
        int written = 0;
        while (it.hasNext()) {
            Function f = it.next();
            String name = f.getName();
            boolean hit = keys.isEmpty();
            for (String k : keys) {
                if (name.contains(k)) {
                    hit = true;
                    break;
                }
            }
            if (!hit) {
                continue;
            }
            try {
                DecompileResults res = dec.decompileFunction(f, 180, monitor);
                if (res != null && res.decompileCompleted()) {
                    String c = res.getDecompiledFunction().getC();
                    String safe = name.replaceAll("[^A-Za-z0-9_.-]", "_");
                    if (safe.length() > 110) {
                        safe = safe.substring(0, 110);
                    }
                    File out = new File(dir, safe + "_" + f.getEntryPoint() + ".c");
                    PrintWriter pw = new PrintWriter(out, "UTF-8");
                    try {
                        pw.println("// " + name + " @ " + f.getEntryPoint()
                                + "  size=" + f.getBody().getNumAddresses());
                        pw.print(c);
                    } finally {
                        pw.close();
                    }
                    println("[+] " + name + " @ " + f.getEntryPoint() + " -> " + out.getName());
                    written++;
                } else {
                    println("[-] decompile failed: " + name);
                }
            } catch (Exception ex) {
                println("[!] " + name + " : " + ex.getMessage());
            }
            if (written >= max) {
                break;
            }
        }
        println("[=] decompiled " + written + " function(s)");
    }
}

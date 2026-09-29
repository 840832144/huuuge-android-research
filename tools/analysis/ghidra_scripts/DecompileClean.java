// Ghidra headless postScript —— 清理误判的 noReturn 标志后反编译指定地址
//
// 背景：libBigCasino.so 的导入调用大量走 PLT，Ghidra 的 "Non-Returning Functions -
// Discovered" 分析会把某些被调函数误判为"不返回"，于是反编译输出里出现
// "/* WARNING: Subroutine does not return */" 并且控制流被截断 → 伪代码失去意义。
// 本脚本先清掉 noReturn（可只对指定关键字/全部），再用 ELF 符号表真实 size 强制函数体，
// 最后反编译。诊断时打印被清掉的数量，便于判断影响面。
//
// 用法:
//   -postScript DecompileClean.java <outdir> <addr:size ...> [--keep-noreturn]
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.address.AddressSet;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionIterator;
import ghidra.program.model.listing.FunctionManager;
import ghidra.program.model.symbol.SourceType;

import java.io.File;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;

public class DecompileClean extends GhidraScript {

    @Override
    public void run() throws Exception {
        String outdir = ".";
        boolean keepNoReturn = false;
        List<String> pairs = new ArrayList<>();
        for (String a : getScriptArgs()) {
            String t = a.trim();
            if (t.isEmpty()) {
                continue;
            }
            if (t.equals("--keep-noreturn")) {
                keepNoReturn = true;
            } else if (t.matches("^[A-Za-z]:[\\\\/].*") || t.startsWith("/")) {
                outdir = t;
            } else if (t.contains(":")) {
                pairs.add(t);
            }
        }

        File dir = new File(outdir);
        if (!dir.isDirectory()) {
            dir.mkdirs();
        }

        FunctionManager fm = currentProgram.getFunctionManager();

        // 1) 清理误判的 noReturn
        if (!keepNoReturn) {
            int cleared = 0;
            List<String> sample = new ArrayList<>();
            FunctionIterator it = fm.getFunctions(true);
            while (it.hasNext()) {
                Function f = it.next();
                if (f.hasNoReturn()) {
                    f.setNoReturn(false);
                    cleared++;
                    if (sample.size() < 8) {
                        sample.add(f.getName());
                    }
                }
            }
            println("[*] cleared noReturn on " + cleared + " function(s); sample=" + sample);
        }

        // 2) 强制函数体 + 反编译
        DecompInterface dec = new DecompInterface();
        dec.openProgram(currentProgram);
        println("[*] program : " + currentProgram.getName() + "  imagebase=" + currentProgram.getImageBase());

        int written = 0;
        for (String pair : pairs) {
            String[] parts = pair.split(":");
            if (parts.length != 2) {
                continue;
            }
            long addrVal = Long.decode(parts[0]);
            long size = Long.decode(parts[1]);
            Address entry = currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(addrVal);
            if (entry == null) {
                println("[!] bad address " + parts[0]);
                continue;
            }

            Function fn = fm.getFunctionAt(entry);
            long curSize = fn == null ? -1 : fn.getBody().getNumAddresses();
            if (fn != null && curSize != size) {
                println("[*] fixing body: " + fn.getName() + "  " + curSize + " -> " + size);
                fm.removeFunction(entry);
                fn = null;
            }
            if (fn == null) {
                AddressSet body = new AddressSet(entry, entry.add(size - 1));
                try {
                    fn = fm.createFunction(null, entry, body, SourceType.USER_DEFINED);
                } catch (Exception ex) {
                    println("[!] createFunction failed at " + entry + " : " + ex.getMessage());
                    continue;
                }
            }
            if (fn == null) {
                println("[!] cannot materialise function at " + entry);
                continue;
            }
            if (fn.hasNoReturn()) {
                fn.setNoReturn(false);
            }

            DecompileResults res = dec.decompileFunction(fn, 300, monitor);
            if (res == null || !res.decompileCompleted()) {
                println("[-] decompile failed: " + fn.getName());
                continue;
            }
            String c = res.getDecompiledFunction().getC();
            String safe = fn.getName().replaceAll("[^A-Za-z0-9_.-]", "_");
            if (safe.length() > 100) {
                safe = safe.substring(0, 100);
            }
            File out = new File(dir, safe + "_" + fn.getEntryPoint() + ".c");
            PrintWriter pw = new PrintWriter(out, "UTF-8");
            try {
                pw.println("// " + fn.getName() + " @ " + fn.getEntryPoint()
                        + "  size=" + fn.getBody().getNumAddresses() + "  (ELF size, noReturn cleared)");
                pw.print(c);
            } finally {
                pw.close();
            }
            println("[+] " + out.getName() + "  (" + c.length() + " chars)");
            written++;
        }
        println("[=] decompiled " + written + " function(s)");
    }
}

// Ghidra headless postScript —— 按"地址:长度"强制修正函数体后反编译
//
// 为什么需要它：libBigCasino.so 的 GOT/PLT 与函数重叠较多，Ghidra 的流分析会把某些
// 函数体切得过小（例如 findMostOccupiedSlots 只识别出 58 字节，而 ELF 符号表写 983）。
// 这里用 elf_triage.py 从 .dynsym 读到的真实 size 强制重建函数体，再反编译。
//
// 用法（Ghidra 会把参数按逗号/空格切开，所以每个"地址:长度"是一个独立参数）:
//   -postScript DecompileRange.java <outdir> 0x78e230:571 0x78e180:169 ...
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.address.AddressSet;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionManager;
import ghidra.program.model.symbol.SourceType;

import java.io.File;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;

public class DecompileRange extends GhidraScript {

    @Override
    public void run() throws Exception {
        String outdir = ".";
        List<String> pairs = new ArrayList<>();
        for (String a : getScriptArgs()) {
            String t = a.trim();
            if (t.isEmpty()) {
                continue;
            }
            if (t.matches("^[A-Za-z]:[\\\\/].*") || t.startsWith("/")) {
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
        DecompInterface dec = new DecompInterface();
        dec.openProgram(currentProgram);

        println("[*] program : " + currentProgram.getName() + "  imagebase=" + currentProgram.getImageBase());
        println("[*] outdir  : " + dir.getAbsolutePath());
        println("[*] targets : " + pairs.size());

        int written = 0;
        for (String pair : pairs) {
            String[] parts = pair.split(":");
            if (parts.length != 2) {
                println("[!] bad pair: " + pair);
                continue;
            }
            long addrVal = Long.decode(parts[0]);
            long size = Long.decode(parts[1]);
            Address entry = currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(addrVal);
            if (entry == null) {
                println("[!] bad address: " + parts[0]);
                continue;
            }

            String oldName = "?";
            Function existing = fm.getFunctionAt(entry);
            if (existing != null) {
                oldName = existing.getName();
                if (existing.getBody().getNumAddresses() != size) {
                    println("[*] fixing body: " + oldName + "  " + existing.getBody().getNumAddresses()
                            + " -> " + size + " bytes");
                    fm.removeFunction(entry);
                    existing = null;
                }
            }
            Function fn = existing;
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
                println("[!] could not materialise function at " + entry);
                continue;
            }
            println("[*] function: " + fn.getName() + " @ " + fn.getEntryPoint()
                    + "  body=" + fn.getBody().getNumAddresses());

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
                        + "  size=" + fn.getBody().getNumAddresses()
                        + "  (body forced from ELF symbol size)");
                pw.print(c);
            } finally {
                pw.close();
            }
            println("[+] wrote " + out.getAbsolutePath() + "  (" + c.length() + " chars)");
            written++;
        }
        println("[=] decompiled " + written + " function(s)");
    }
}

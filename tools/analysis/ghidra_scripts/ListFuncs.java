// Ghidra headless postScript —— 列出函数（地址/大小/名字）
// 用法: -postScript ListFuncs.java <关键字...> [max]
// 注意：Ghidra 会把脚本参数按【逗号和空格】都切开，所以这里把所有"非纯数字"参数
// 都当关键字，最后一个纯数字参数当上限。不要用 | 或逗号拼关键字。
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionIterator;

import java.util.ArrayList;
import java.util.List;

public class ListFuncs extends GhidraScript {

    @Override
    public void run() throws Exception {
        List<String> keys = new ArrayList<>();
        int max = 200;
        for (String a : getScriptArgs()) {
            String t = a.trim();
            if (t.isEmpty()) {
                continue;
            }
            if (t.matches("\\d+")) {
                max = Integer.parseInt(t);
            } else {
                keys.add(t);
            }
        }

        FunctionIterator it = currentProgram.getFunctionManager().getFunctions(true);
        int total = 0;
        int shown = 0;

        println("[*] program   : " + currentProgram.getName());
        println("[*] imagebase : " + currentProgram.getImageBase());
        println("[*] functions : " + currentProgram.getFunctionManager().getFunctionCount());
        println("[*] keys      : " + keys);

        while (it.hasNext()) {
            Function f = it.next();
            total++;
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
            println("FUNC " + f.getEntryPoint() + "  size=" + f.getBody().getNumAddresses() + "  " + name);
            shown++;
            if (shown >= max) {
                break;
            }
        }
        println("[=] scanned=" + total + " matched=" + shown + " (limit " + max + ")");
    }
}
